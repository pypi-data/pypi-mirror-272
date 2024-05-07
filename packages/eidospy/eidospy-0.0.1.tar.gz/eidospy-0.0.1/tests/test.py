from eidospy import Eidos

if __name__ == "__main__":
    eidos = Eidos("https://api.eidos.space/rpc/585067c5-d5e3-4e05-bf60-ba69d75eb7c7")
    space = eidos.space("eidos3")
    table = space.table("67d7857386544a30ae312ee4509e0e17")
    res = table.rows.query({}, {})
    print(res)
