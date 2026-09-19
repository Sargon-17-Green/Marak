class ContractError(ValueError): pass

def validate(units):
    places=set(); acts=set(); roles=set(); bodies=set(); execs=0; started=False
    def ref(r):
        k=r[0]
        if k=='place' and r[1] not in places: raise ContractError('REFERENCE_BEFORE_INTRODUCTION')
        if k=='act' and r[1] not in acts: raise ContractError('REFERENCE_BEFORE_INTRODUCTION')
        if k=='role' and (r[1],r[2]) not in roles: raise ContractError('REFERENCE_BEFORE_INTRODUCTION')
        if k=='current_role_outside': raise ContractError('ROLE_VALUE_OUTSIDE_PERFORMANCE')
    for u in units:
        k=u[0]
        if k=='exec':
            execs+=1
            if execs>1: raise ContractError('MULTIPLE_PRINCIPAL_EXECUTION')
            started=True
            if u[2]>1 and not u[3]: raise ContractError('UNSEQUENCED_TOP_ACTIONS')
            for r in u[1]: ref(r)
            continue
        if started: raise ContractError('PREPARATORY_UNIT_AFTER_EXECUTION')
        if k=='place':
            if u[1] in places: raise ContractError('DUPLICATE_PLACE')
            places.add(u[1])
        elif k=='act':
            if u[1] in acts: raise ContractError('DUPLICATE_ACT')
            acts.add(u[1])
        elif k=='role':
            owner,name=u[1],u[2]
            if owner not in acts: raise ContractError('ROLE_OWNER_NOT_INTRODUCED')
            if owner in bodies: raise ContractError('ROLE_AFTER_BODY')
            if (owner,name) in roles: raise ContractError('DUPLICATE_ROLE')
            roles.add((owner,name))
        elif k=='body':
            name=u[1]
            if name not in acts: raise ContractError('BODY_OWNER_NOT_INTRODUCED')
            if name in bodies: raise ContractError('DUPLICATE_BODY')
            for r in u[2]: ref(r)
            bodies.add(name)
        elif k=='body_noncore':
            if u[2]=='חדל': raise ContractError('NO_HALT_SURFACE')
        elif k=='invalid_negative': raise ContractError('NEGATIVE_LITERAL_NOT_ADMITTED')
        else: raise ContractError('UNKNOWN_UNIT')
    if execs==0: raise ContractError('NO_PRINCIPAL_EXECUTION')
    if acts!=bodies: raise ContractError('MISSING_ACT_BODY')
    return True
