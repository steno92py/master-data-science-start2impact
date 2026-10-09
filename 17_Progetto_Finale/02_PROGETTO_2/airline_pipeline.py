"""Trasformazioni apprese soltanto sui dati passati a fit, anche dentro la CV."""
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind, chi2_contingency
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler, RobustScaler
from sklearn.impute import SimpleImputer
from sklearn.utils.validation import check_is_fitted

RATINGS = [
    'Inflight wifi service', 'Departure/Arrival time convenient',
    'Ease of Online booking', 'Gate location', 'Food and drink',
    'Online boarding', 'Seat comfort', 'Inflight entertainment',
    'On-board service', 'Leg room service', 'Baggage handling',
    'Checkin service', 'Inflight service', 'Cleanliness',
]
DELAYS = ['Departure Delay in Minutes', 'Arrival Delay in Minutes']
NUMERIC = ['Age', 'Flight Distance'] + DELAYS + RATINGS
CATEGORICAL = ['Gender', 'Customer Type', 'Type of Travel', 'Class']
PRE_FLIGHT = ['Age', 'Flight Distance'] + CATEGORICAL


def welch_ranking(X, y):
    """Welch sui valori osservati; gli zeri dei rating sono esclusi come N/A."""
    labels = np.asarray(y)
    rows = []
    for column in NUMERIC:
        values = pd.to_numeric(X[column], errors='raise')
        if column in RATINGS:
            values = values.replace(0, np.nan)
        group0 = values.iloc[np.flatnonzero(labels == 0)].dropna()
        group1 = values.iloc[np.flatnonzero(labels == 1)].dropna()
        if len(group0) < 2 or len(group1) < 2 or (group0.var() == 0 and group1.var() == 0):
            stat, p = 0.0, 1.0
        else:
            stat, p = ttest_ind(group0, group1, equal_var=False)
        rows.append({'feature': column, 't_stat': abs(float(stat)), 'p_value': float(p),
                     'n0': len(group0), 'n1': len(group1)})
    return (pd.DataFrame(rows).set_index('feature')
            .sort_values(['t_stat'], ascending=False, kind='stable'))


class SurveySelector(TransformerMixin, BaseEstimator):
    """T-test obbligatorio, confronto ibrido, oppure colonne fissate a priori."""
    def __init__(self, method='ttest', k=4, alpha=0.05, columns=None):
        self.method = method
        self.k = k
        self.alpha = alpha
        self.columns = columns

    def fit(self, X, y=None):
        self.n_fit_rows_ = len(X)
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        self.class_to_business_ = False
        if self.method == 'fixed':
            self.selected_features_ = list(self.columns)
        elif self.method in ('ttest', 'hybrid'):
            self.ranking_ = welch_ranking(X, y)
            significant = self.ranking_.query('p_value < @self.alpha')
            required = self.k if self.method == 'ttest' else 2
            if len(significant) < required:
                raise ValueError(f'Solo {len(significant)} variabili significative; ne servono {required}.')
            self.selected_features_ = significant.head(required).index.tolist()
            if self.method == 'hybrid':
                scores = {}
                for col in CATEGORICAL:
                    table = pd.crosstab(X[col].fillna('Mancante'), np.asarray(y))
                    dimension = min(table.shape) - 1
                    scores[col] = (np.sqrt(chi2_contingency(table)[0] / (table.values.sum() * dimension))
                                   if dimension > 0 else 0.0)
                self.categorical_ranking_ = pd.Series(scores).sort_values(ascending=False, kind='stable')
                self.selected_features_ += self.categorical_ranking_.head(2).index.tolist()
                self.class_to_business_ = 'Class' in self.selected_features_
        else:
            raise ValueError(f'Metodo non previsto: {self.method}')
        return self

    def transform(self, X):
        check_is_fitted(self, 'selected_features_')
        result = X.loc[:, self.selected_features_].copy()
        if self.class_to_business_:
            result['Class_Business'] = (result.pop('Class') == 'Business').astype(float)
        return result

    def get_feature_names_out(self, input_features=None):
        names = list(self.selected_features_)
        if self.class_to_business_:
            names.remove('Class')
            names.append('Class_Business')
        return np.asarray(names, dtype=object)


class SurveyPreprocessor(TransformerMixin, BaseEstimator):
    """Mediane, categorie e scaler conservati insieme per inferenza da righe grezze."""
    def __init__(self, add_zero_flags=True):
        self.add_zero_flags = add_zero_flags

    def _numeric(self, X):
        result = X.loc[:, self.numeric_].astype(float).copy()
        for col in self.rating_columns_:
            result[col] = result[col].replace(0, np.nan)
        return result

    def fit(self, X, y=None):
        self.n_fit_rows_ = len(X)
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        self.categorical_ = [c for c in X if c in CATEGORICAL]
        self.numeric_ = [c for c in X if c not in self.categorical_]
        self.rating_columns_ = [c for c in self.numeric_ if c in RATINGS]
        self.zero_columns_ = [c for c in self.rating_columns_ if (X[c] == 0).any()] if self.add_zero_flags else []
        self.robust_ = [c for c in self.numeric_ if c in DELAYS]
        self.standard_ = [c for c in self.numeric_ if c not in DELAYS]
        self.imputer_ = SimpleImputer(strategy='median', keep_empty_features=True)
        numeric = pd.DataFrame(self.imputer_.fit_transform(self._numeric(X)), columns=self.numeric_, index=X.index)
        self.robust_scaler_ = RobustScaler().fit(numeric[self.robust_]) if self.robust_ else None
        self.standard_scaler_ = StandardScaler().fit(numeric[self.standard_]) if self.standard_ else None
        if self.categorical_:
            self.category_imputer_ = SimpleImputer(strategy='most_frequent', keep_empty_features=True)
            categories = self.category_imputer_.fit_transform(X[self.categorical_])
            self.encoder_ = OneHotEncoder(drop='if_binary', handle_unknown='ignore', sparse_output=False)
            self.encoder_.fit(categories)
        names = self.numeric_ + [c + '_zeroflag' for c in self.zero_columns_]
        if self.categorical_:
            names += self.encoder_.get_feature_names_out(self.categorical_).tolist()
        self.output_features_ = np.asarray(names, dtype=object)
        return self

    def transform(self, X):
        check_is_fitted(self, 'output_features_')
        result = pd.DataFrame(self.imputer_.transform(self._numeric(X)), columns=self.numeric_, index=X.index)
        if self.robust_:
            result.loc[:, self.robust_] = self.robust_scaler_.transform(result[self.robust_])
        if self.standard_:
            result.loc[:, self.standard_] = self.standard_scaler_.transform(result[self.standard_])
        for col in self.zero_columns_:
            result[col + '_zeroflag'] = (X[col] == 0).astype(float)
        if self.categorical_:
            values = self.category_imputer_.transform(X[self.categorical_])
            encoded = self.encoder_.transform(values)
            result = pd.concat([result, pd.DataFrame(encoded, index=X.index,
                                columns=self.encoder_.get_feature_names_out(self.categorical_))], axis=1)
        return result.loc[:, self.output_features_]

    def get_feature_names_out(self, input_features=None):
        check_is_fitted(self, 'output_features_')
        return self.output_features_.copy()
