
def name_ex(name: str) -> str:    
    ster = name.find("file_path='") + len("file_path='")
    end  = name.find("'", ster)
    name = name[ster:end]    
    return name

