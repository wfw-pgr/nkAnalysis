import numpy as np

# ========================================================= #
# ===  extract Data on plain                            === #
# ========================================================= #

def extract__data_onPlain():

    # ------------------------------------------------- #
    # --- [1] Load constants / Data                 --- #
    # ------------------------------------------------- #
    import nkUtilities.load__constants as lcn
    cnsFile = "dat/parameter.conf"
    const   = lcn.load__constants( inpFile=cnsFile )

    import nkUtilities.load__pointFile as lpf
    Data    = lpf.load__pointFile( inpFile=const["inpFile"], returnType="point" )
    
    # ------------------------------------------------- #
    # --- [2] settings axis                         --- #
    # ------------------------------------------------- #
    if   ( const["axis"].lower() == "x" ):
        ref_ = 0
    elif ( const["axis"].lower() == "y" ):
        ref_ = 1
    elif ( const["axis"].lower() == "z" ):
        ref_ = 2

    # ------------------------------------------------- #
    # --- [3] data extraction                       --- #
    # ------------------------------------------------- #
    import nkBasicAlgs.extract__pointData as ext
    ret = ext.extract__pointData( Data=Data, ref_=ref_, value=const["value"] )

    # ------------------------------------------------- #
    # --- [4] save in a file                        --- #
    # ------------------------------------------------- #
    import nkUtilities.save__pointFile as spf
    spf.save__pointFile( outFile=const["outFile"], Data=ret )
    
    return()



# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #
if ( __name__=="__main__" ):
    ret = extract__data_onPlain()

    

