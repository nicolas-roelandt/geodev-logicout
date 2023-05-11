import matplotlib.pyplot as plt
import numpy as np
import use_data
import IsInclude
import os


def histo(filename, dictFilename, dist, type, dictType, path):
    fullpath= f"{path}_histo_{dictFilename[filename]}_{str(dist*1e-3).removesuffix('.0')}_{dictType[type]}.png"
       
    gdf = use_data.create_gdf(filename, 'cheflieu') # dataframe du fichier csv choisi
    n = gdf.count()[0] # number of total rounds
    A = []
    for i in range(n):
        tournee = gdf.iloc[[i]]
        gdf_IsInclude = IsInclude.IsIn_tournee_gdf(tournee, gdf, dist, type)
        nbrMutu = gdf_IsInclude.count()[0]
        A.append(nbrMutu)

    # affichage de l'histogramme
    plt.hist(A,bins=20,color="blue",edgecolor="gray",label="histogramme")
    plt.title('Histogramme du nombre de mutualisations possibles : tournées '+dictFilename[filename])
    plt.xlabel('Nombre de tournées dans un rayon de '+str(dist*1e-3)+' km pour des utilisateurs différents ('+dictType[type]+' inclusion)')
    plt.ylabel('Fréquence')
    plt.rcParams['svg.fonttype'] = 'none'
    plt.savefig(fullpath)
    #plt.show()
    return 'Histogramme [ '+dictFilename[filename]+' '+dictType[type]+' '+str(dist*1e-3)+' ] tracé !'



def histo_comparaison(single_inclusion, double_inclusion, type):

    labels = ['50 km', '100 km', '150 km']

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, single_inclusion, width, label='simple inclusion', color='deepskyblue')
    rects2 = ax.bar(x + width/2, double_inclusion, width, label='double inclusion', color='mediumorchid')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel("km du rayon considéré")
    if type == 'Pas':
        ax.set_ylabel("% de tournées mutualisables") # i.e. ayant au moins une tournée dans son buffer
    if type == 'Mean':
        ax.set_ylabel("nombre de tournées moyennes dans un rayon de X km")
    if type == 'Max':
        ax.set_ylabel("nombre maximum de tournées dans un rayon de X km")
    ax.set_title('Comparaison entre une simple et une double inclusion, pour des rayons différents')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    autolabel(rects1, ax)
    autolabel(rects2, ax)
    fig.tight_layout()
    #plt.show()
    return 'Tracé effectué !'

def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

def mutu(filename, dist):
    gdf = use_data.create_gdf(filename, 'cheflieu') # dataframe du fichier csv choisi
    n = gdf.count()[0] # number of total rounds
    L1 = []
    L2 = []
    for j in range(1,3):
        for d in dist:
            pas_mutu = 0
            for i in range(n):
                tournee = gdf.iloc[[i]]
                gdf_IsInclude = IsInclude.IsIn_tournee_gdf(tournee, gdf, d, j)
                if gdf_IsInclude.count()[0] != 0:
                    pas_mutu += 1
            if j == 1:
                L1.append(int(pas_mutu * 100 / n))
            if j == 2:
                L2.append(int(pas_mutu * 100 / n))
    return L1, L2

def mean_mutu(filename, dist):
    gdf = use_data.create_gdf(filename, 'cheflieu') # dataframe du fichier csv choisi
    n = gdf.count()[0] # number of total rounds
    L1 = []
    L2 = []
    for j in range(1,3):
        for d in dist:
            mean_mutu = 0
            for i in range(n):
                tournee = gdf.iloc[[i]]
                gdf_IsInclude = IsInclude.IsIn_tournee_gdf(tournee, gdf, d, j)
                mean_mutu += gdf_IsInclude.count()[0]
            mean_mutu = mean_mutu / n
            if j == 1:
                L1.append(int(mean_mutu))
            if j == 2:
                L2.append(int(mean_mutu))
    return L1, L2

def max_mutu(filename, dist):
    gdf = use_data.create_gdf(filename, 'cheflieu') # dataframe du fichier csv choisi
    n = gdf.count()[0] # number of total rounds
    L1 = []
    L2 = []
    for j in range(1,3):
        for d in dist:
            max_mutu = 0
            for i in range(n):
                tournee = gdf.iloc[[i]]
                gdf_IsInclude = IsInclude.IsIn_tournee_gdf(tournee, gdf, d, j)
                mutu = gdf_IsInclude.count()[0]
                if mutu > max_mutu:
                    max_mutu = mutu
            if j == 1:
                L1.append(int(max_mutu))
            if j == 2:
                L2.append(int(max_mutu))
    return L1, L2

if __name__ == "__main__":
    #filenames = ["simulations_reel_gdf.csv", "simulations_gdf.csv"]
    filenames = ["simulations_reel_gdf.csv"] # real simulations only
    filename = "simulations_reel_gdf.csv"
    dictFilename = {"simulations_reel_gdf.csv": "reelles", "simulations_gdf.csv": "quelconques"}
    dist = [50e3, 100e3, 150e3]
    typeIsIn = [1, 2]
    dictType = {1:"simple", 2:"double"}

    ###      Tracer les histogrammes      ###
    root = os.path.join(os.path.dirname( __file__ ), os.pardir)  # relative path to the gitignore directory
    dirname = "/data/results/" # relative path to the gitignore directory - the function on the file _dataframes_gpd.py is adapted to find the relative path of this directory
    print(root+dirname)
    for file in filenames:
        for d in dist:
            for type in typeIsIn:
                print(histo(file, dictFilename, d, type, dictType, path=(root+dirname)))
                #histo(file, dictFilename, d, type, dictType)


    ###      Obtenir des comparaisons quantitatives      ###

    #single_inclusion, double_inclusion = mutu(filename, dist)
    #type = 'Pas'

    #single_inclusion, double_inclusion = mean_mutu(filename, dist)
    #type = 'Mean'

    #single_inclusion, double_inclusion = max_mutu(filename, dist)
    #type = 'Max'

    #print(single_inclusion)
    #print(double_inclusion)
    #print(histo_comparaison(single_inclusion, double_inclusion, type))

