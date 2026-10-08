// Test locali: nessuna chiamata a Telegram, email, calendario o modelli.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const {createRequire} = require('node:module');
const repo = process.env.N8N_REPO;
if (!repo) throw new Error('Imposta N8N_REPO al percorso di una installazione sorgente n8n compilata.');
const req = createRequire(path.join(repo, 'packages/workflow/package.json'));
const {Expression, safeParseWorkflowStructure} = req('./dist/cjs/index.js');
const {DateTime} = req('luxon');
const wf = JSON.parse(fs.readFileSync(path.join(__dirname, 'workflow.json'), 'utf8'));
const nodes = Object.fromEntries(wf.nodes.map(n => [n.name, n]));
const expression = new Expression('Europe/Rome');
const checks = [];
const check = (name, fn) => {fn(); checks.push({name, passed:true});};
const normalize = (json) => vm.runInNewContext(`(function(){${nodes['Normalizza input'].parameters.jsCode}})()`, {
  $input: {first: () => ({json})},
  $: () => ({first: () => ({json:{message:{chat:{id:123}}}})})
});
check('schema n8n reale', () => assert(safeParseWorkflowStructure(wf).success));
check('collegamenti senza nodi inesistenti', () => {
  for(const [source,outputs] of Object.entries(wf.connections)) {
    assert(nodes[source]);
    for(const channels of Object.values(outputs)) for(const channel of channels) for(const edge of channel) assert(nodes[edge.node]);
  }
});
check('testo arriva al prompt', () => {
  const json=normalize({message:{text:'  Crea una bozza  '}})[0].json;
  assert.equal(expression.resolveSimpleParameterValue(nodes['AI Agent'].parameters.text, {$json:json}), 'Crea una bozza');
});
check('trascrizione senza message arriva al prompt', () => {
  const json=normalize({text:'Appuntamento domani alle 15'})[0].json;
  assert.equal(expression.resolveSimpleParameterValue(nodes['AI Agent'].parameters.text, {$json:json}), 'Appuntamento domani alle 15');
});
check('trascrizione vuota respinta', () => assert.throws(() => normalize({text:' '}), /vuoti/));
check('input eccessivo respinto', () => assert.throws(() => normalize({text:'a'.repeat(12001)}), /troppo lungo/));
check('data corrente risolta dal motore n8n', () => {
  const text=expression.resolveSimpleParameterValue(nodes['AI Agent'].parameters.options.systemMessage, {$now:DateTime.fromISO('2026-10-07T13:00:00+02:00')});
  assert(text.includes('2026-10-07T13:00:00.000+02:00'));
  assert(!text.includes('{{'));
});
check('invitati calendario come array, anche vuoto', () => {
  const value=nodes['calendario'].parameters.additionalFields.attendees;
  for(const [input,expected] of [['a@example.com, b@example.com',['a@example.com','b@example.com']],['',[]]]) {
    const actual=expression.resolveSimpleParameterValue(value, {$fromAI:()=>input});
    assert.deepEqual(Array.from(actual),expected);
  }
});
check('risposta Telegram con caratteri HTML letterali', () => {
  const actual=expression.resolveSimpleParameterValue(nodes['Telegram Send'].parameters.text,{$json:{output:'A < B & C'}});
  assert.equal(actual,'A &lt; B &amp; C');
});
check('chat non autorizzate e gruppi esclusi', () => {
  const source=nodes['Solo Stefano'].parameters.jsCode.replace('INSERISCI_CHAT_ID','123');
  const items=[{json:{message:{chat:{id:123,type:'private'}}}},{json:{message:{chat:{id:456,type:'private'}}}},{json:{message:{chat:{id:123,type:'group'}}}}];
  const result=vm.runInNewContext(`(function(){${source}})()`,{$input:{all:()=>items}});
  assert.equal(result.length,1);assert.equal(result[0].json.message.chat.id,123);
});
check('assenza configurazione blocca accesso', () => assert.throws(() => vm.runInNewContext(`(function(){${nodes['Solo Stefano'].parameters.jsCode}})()`,{}),/Configura/));
check('workflow esportato inattivo e senza credenziali', () => {assert.equal(wf.active,false); assert(wf.nodes.every(n=>!n.credentials));});
const report={date:'2026-10-07',n8nVersion:req('./package.json').version,liveExternalCalls:false,checks};
fs.mkdirSync(path.join(__dirname,'evidenze'),{recursive:true});
fs.writeFileSync(path.join(__dirname,'evidenze/test_workflow.json'),JSON.stringify(report,null,2)+'\n');
console.log(`${checks.length} controlli superati con il motore n8n ${report.n8nVersion}; nessuna chiamata esterna.`);
