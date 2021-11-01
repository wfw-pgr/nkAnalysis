import numpy                    as np
import nkUtilities.plot1D       as pl1
import nkUtilities.load__config as lcf

# ========================================================= #
# ===  display__radialplot_from2DGrid.py                === #
# ========================================================= #

def display__radialplot_from2DGrid():

    x_,y_,z_ = 0, 1, 2
    
    # ------------------------------------------------- #
    # --- [1] load constants                        --- #
    # ------------------------------------------------- #
    import nkUtilities.load__constants as lcn
    cnsFile   = "dat/parameter.conf"
    const     = lcn.load__constants( inpFile=cnsFile )

    # ------------------------------------------------- #
    # --- [2] load data                             --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    Data      = lpf.load__pointFile( inpFile=const["inpFile"], returnType="point" )
    size      = (const["LJ"],const["LI"],3)
    gridData  = np.concatenate( [ Data[:,0:2], ( Data[:,const["index"] ])[:,None] ], axis=1 )
    gridData  = np.reshape( gridData, size )

    # ------------------------------------------------- #
    # --- [3] generate radial points                --- #
    # ------------------------------------------------- #

    if   ( const["pointType"].lower() == "radius" ):
        import nkBasicAlgs.generate__line_coord as glc
        theta     = ( const["theta"] - 90.0 ) / 180.0 * np.pi
        x1        = [ const["xc"][x_] + const["radius1"]*np.cos( theta ), \
                      const["xc"][y_] + const["radius1"]*np.sin( theta ), \
                      const["xc"][z_] ]
        x2        = [ const["xc"][x_] + const["radius2"]*np.cos( theta ), \
                      const["xc"][y_] + const["radius2"]*np.sin( theta ), \
                      const["xc"][z_] ]
        pointData = glc.generate__line_coord( x1=x1, x2=x2, nDiv=const["nDiv"] )
        radii     = np.linspace( const["radius1"], const["radius2"], const["nDiv"] )

    elif ( const["pointType"].lower() == "arc"    ):
        import nkBasicAlgs.generate__arc_coord as gac
        pointData = gac.generate__arc_coord( xc =const["xc"]    , radius=const["radius"], \
                                             th1=const["theta1"], th2   =const["theta2"], \
                                             nDiv=const["nDiv"] )
        theta     = np.linspace( const["theta1"], const["theta2"], const["nDiv"] )

    else:
        print( "[display__radialplot_from2DGrid.py] unknown pointType. " )
        sys.exit()

    
    # ------------------------------------------------- #
    # --- [4] interpolation                         --- #
    # ------------------------------------------------- #
    import nkInterpolator.interpolate__grid2point as g2p
    ret       = g2p.interpolate__grid2point( gridData=gridData, pointData=pointData )

    # ------------------------------------------------- #
    # --- [5] save in a file                        --- #
    # ------------------------------------------------- #
    if   ( const["pointType"].lower() == "radius" ):
        wData = np.concatenate( [ret,radii[:,None]], axis=1 )
    elif ( const["pointType"].lower() == "arc"  ):
        wData = np.concatenate( [ret,theta[:,None]], axis=1 )
    else:
        print( "[display__radialplot_from2DGrid.py] unknown pointType. " )
        sys.exit()
    
    import nkUtilities.save__pointFile as spf
    spf.save__pointFile( outFile=const["outFile"], Data=wData )

    # ------------------------------------------------- #
    # --- [6] draw plot                             --- #
    # ------------------------------------------------- #
    v_,r_   = 2, 3
    config  = lcf.load__config()
    config  = dict( config, **const )
    
    fig     = pl1.plot1D( config=config, pngFile=const["pngFile"] )
    fig.add__plot( xAxis=wData[:,r_], yAxis=wData[:,v_] )
    fig.set__axis()
    fig.save__figure()


    
    return()


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    test = True
    if ( test ):
        import nkUtilities.equiSpaceGrid as esg
        x1MinMaxNum = [ -1.0, 1.0, 51 ]
        x2MinMaxNum = [ -1.0, 1.0, 51 ]
        x3MinMaxNum = [  0.0, 0.0,  1 ]
        ret         = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                         x3MinMaxNum=x3MinMaxNum, returnType = "point" )
        radii       = np.sqrt( ret[:,0]**2 + ret[:,1]**2 )
        zeros       = np.zeros( (radii.shape[0],1) )
        Data        = np.concatenate( [ret,zeros,zeros,radii[:,None]], axis=1 )

        import nkUtilities.save__pointFile as spf
        spf.save__pointFile( outFile="dat/testgrid.dat", Data=Data )
        
    display__radialplot_from2DGrid()
