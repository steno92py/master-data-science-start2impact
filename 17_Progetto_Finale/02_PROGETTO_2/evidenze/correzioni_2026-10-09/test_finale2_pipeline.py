import sys, json, pathlib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import joblib

W=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(W))
from airline_pipeline import SurveySelector, SurveyPreprocessor, NUMERIC, CATEGORICAL, PRE_FLIGHT, DELAYS
raw=pd.read_csv(W/'train.csv')
X=raw[NUMERIC+CATEGORICAL].head(3000)
y=(raw['satisfaction'].head(3000)=='satisfied').astype(int)

def test_holdout_never_changes_fitted_statistics():
    train,valid=next(StratifiedKFold(5,shuffle=True,random_state=0).split(X,y))
    prep=SurveyPreprocessor().fit(X.iloc[train])
    before=prep.imputer_.statistics_.copy()
    v=X.iloc[valid].copy();v['Age']=1_000_000;v['Arrival Delay in Minutes']=np.nan
    assert np.isfinite(prep.transform(v).to_numpy()).all()
    assert np.array_equal(before,prep.imputer_.statistics_)
    actual=prep.standard_scaler_.mean_[prep.standard_.index('Age')]
    assert np.isclose(actual,X.iloc[train]['Age'].mean())
    assert not np.isclose(actual,X['Age'].mean())
    assert prep.n_fit_rows_==len(train)

def test_cv_refits_selector_and_preprocessor_inside_each_fold():
    p=Pipeline([('select',SurveySelector()),('prepare',SurveyPreprocessor(False)),('model',DecisionTreeClassifier(max_depth=3,random_state=0))])
    result=cross_validate(p,X,y,cv=StratifiedKFold(3,shuffle=True,random_state=0),return_estimator=True,error_score='raise')
    for fitted in result['estimator']:
        assert fitted['select'].n_fit_rows_==2000
        assert fitted['prepare'].n_fit_rows_==2000
        columns=fitted['prepare'].get_feature_names_out()
        assert len(columns)==4
        assert (fitted['select'].ranking_.loc[columns,'p_value']<.05).all()
        assert set(columns).issubset(NUMERIC)
    assert not hasattr(p['select'],'selected_features_')

def test_raw_input_roundtrip_and_column_order(tmp_path):
    p=Pipeline([('prepare',SurveyPreprocessor()),('model',DecisionTreeClassifier(max_depth=3,random_state=0))]).fit(X,y)
    sample=X.tail(5).copy()
    sample.iloc[0,sample.columns.get_loc('Arrival Delay in Minutes')]=np.nan
    sample.iloc[1,sample.columns.get_loc('Class')]='Nuova'
    sample.iloc[2,sample.columns.get_loc('Online boarding')]=0
    before=sample.copy(deep=True)
    probabilities=p.predict_proba(sample)
    assert np.isfinite(probabilities).all()
    pd.testing.assert_frame_equal(before,sample)
    path=tmp_path/'model.joblib';joblib.dump(p,path)
    loaded=joblib.load(path)
    assert np.allclose(probabilities,loaded.predict_proba(sample[sample.columns[::-1]]))

def test_preflight_cannot_use_actual_delays_or_ratings():
    selector=SurveySelector(method='fixed',columns=PRE_FLIGHT).fit(X,y)
    base=selector.transform(X)
    changed=X.copy();changed[DELAYS]=123456
    pd.testing.assert_frame_equal(base,selector.transform(changed))
    assert base.shape[1]==6

def test_hybrid_preserves_four_model_columns():
    p=Pipeline([('select',SurveySelector(method='hybrid')),('prepare',SurveyPreprocessor(False))]).fit(X,y)
    assert p.transform(X).shape==(len(X),4)
    assert 'Class_Business' in p['prepare'].get_feature_names_out()

def test_notebook_has_original_grids_and_all_original_cells():
    import nbformat
    n=nbformat.read(W/'Progetto Finale Data Science di Stefano Nocco.ipynb',as_version=4)
    assert [c.metadata['original_cell'] for c in n.cells if 'original_cell' in c.metadata]==list(range(1,136))
    for c in n.cells:
        if c.cell_type=='code' and not c.source.startswith('%%'):
            compile(c.source,'notebook','exec')
    source='\n'.join(c.source for c in n.cells)
    assert '"n_estimators": [100, 200, 300]' in source
    assert '"max_depth": [3, 5, 7]' in source
    assert "algorithm='SAMME'" not in source
    assert 'warnings.filterwarnings' not in source
