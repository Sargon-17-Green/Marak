# B15 Observable Behavior

B15 adds no new observation category beyond B12+B13.

Observable:
- normal completion;
- defined runtime error;
- divergence;
- semantic state values;
- explicit act-produced outputs under existing provenance;
- B13 representation-independent observation of Symbol, BidirectionalIndex and Collection.

Unobservable:
- Python class/type;
- hidden runtime type tag representation;
- memory address/location;
- Symbol intern index;
- Collection backing array/tree/list, capacity or sharing;
- host stack frame;
- occurrence implementation object;
- result register;
- parser node identity;
- HAST/IR serialization details.

Static domain contracts are semantically significant validation metadata, but their machine
representation is not observable.
