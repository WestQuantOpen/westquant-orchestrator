from westquant_orchestrator import aggregate, normalize_record

def row():
    return {'framework':'x','challenge_id':'c','state_id':'s','next_state_id':'n','step_index':0,'stage':'a','action':{'name':'b'},'success':True,'selectable':True,'verification':{'equivalence':'exact','verified':True},'metrics_before':{'depth':3},'metrics_after':{'depth':2},'kept_in_beam':True,'terminal':False,'error':None}

def test_normalize_and_stats():
    r=normalize_record(row())
    assert r['outcome_class']=='verified_exact'
    s=aggregate([r])
    assert s['n_records']==1 and s['metrics']['depth']['median']==2
