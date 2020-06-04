import sys
import logging
import rds_config
import pymysql
import json
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
#from scipy.ndimage.filters import gaussian_filter

#rds settings
rds_host  = "ips-1.c6mdsdjlgnmm.eu-central-1.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

def handler(event, context):
    # Construct the body of the response object
    responseBody = {}
    #startTime, endTime = event["startTime"], event["endTime"]
    startTime = event['queryStringParameters']['startTime']
    endTime = event['queryStringParameters']['endTime']
    
    """ with conn.cursor() as cur:
        query = f'SELECT * FROM Positions WHERE time>="{startTime}" AND time<"{endTime}"'
        cur.execute(query)
        for row in cur:
            responseBody[row[2]] = {"x": row[3], "y":row[4]}
    """
    
    # initialize heatmap matrix
    heatmap_matrix = [[0 for i in range(4)] for j in range(10)]
    
    with conn.cursor() as cur:
        query = f'SELECT x,y FROM Positions WHERE time>="{startTime}" AND time<"{endTime}"'
        cur.execute(query)
        
        # fill heatmap matrix
        for row in cur:
            heatmap_matrix [row[0]][row[1]] += 1 
            #responseBody[i] = {"x": row[0], "y":row[1]}
            
    ## create heatmap image
    image_filename = "floor_plan.png"
    im = plt.imread(image_filename)
    im = (im*255).astype('uint8')
    
    cmap = [[0.99717032, 0.90136101, 0.85628604],
            [0.99260285, 0.81413303, 0.73837755],
            [0.98823529, 0.70685121, 0.60101499],
            [0.98823529, 0.58579008, 0.4622376 ],
            [0.98572857, 0.47227989, 0.3467897 ],
            [0.96733564, 0.34918877, 0.24775087],
            [0.9256286,  0.2200692,  0.16770473],
            [0.81933103, 0.11672434, 0.12341407],
            [0.71309496, 0.07446367, 0.09625529],
            [0.57936178, 0.04244521, 0.07361784]]
    #cmap123 = sb.cubehelix_palette(rot=5, n_colors=8)
    #cmap123 = sb.color_palette(palette="Reds", n_colors=10)
    cmap = ListedColormap(cmap)
    heatmap = gaussian_filter(heatmap_matrix, sigma=16)
    plt.imshow(255 * heatmap, alpha=5, cmap=cmap123)
    plt.imshow(im)
    logger.info("im:", im)
    conn.commit()
    
    # Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['headers']['Access-Control-Allow-Origin'] = '*'
    responseObject['body'] = json.dumps(responseBody)
 
    # Return the response object
    return responseObject
