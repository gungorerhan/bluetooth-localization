import sys
import logging
import rds_config
import pymysql
import numpy as np
import json
import base64
import os
import io
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.ndimage.filters import gaussian_filter

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
    
    # parse query string parameters 
    startTime = event['queryStringParameters']['startTime']
    endTime = event['queryStringParameters']['endTime']
    
    
    # read image and calculate real distance - image ratios
    image_path = "floor-plan.png"
    im = plt.imread(image_path)
    y, x = im.shape[0]-1, im.shape[1]-1  # 0 indexed
    y_real, x_real = 3.5, 5.25
    x_ratio, y_ratio = x/x_real, y/y_real
    print("X ratio = ", x_ratio)
    print("Y ratio = ", y_ratio)

    # create heatmap matrix
    heatmap = np.zeros((im.shape[0], im.shape[1]))
    
    with conn.cursor() as cur:
        query = f'SELECT x,y FROM Positions WHERE time>={str(startTime)} AND time<{str(endTime)};'
        cur.execute(query)
        
        # fill heatmap matrix
        for row in cur:
            heatmap[round(row[1]*y_ratio)] [round(row[0]*x_ratio)] += 1

    conn.commit()
    
    # create color map (seaborn - Reds)
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
    cmap = ListedColormap(cmap)

    # apply gaussian filter
    hm = gaussian_filter(heatmap, sigma=16).reshape(im.shape[0], im.shape[1])

    # create final image
    plt.imshow(255 * hm, alpha=5, cmap=cmap)
    plt.imshow(im)
    plt.axis("off")
    
    # encode final image
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    final_image = base64.b64encode(buf.read())
    
    return({
        "isBase64Encoded": True,
        "statusCode": 200,
        "headers": {
                "content-type": "image/png",
                "Access-Control-Allow-Origin": "*"
        },  
        'body':  final_image.decode('utf-8')
    })  
