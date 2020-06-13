import xlsxwriter as writer
import operator
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from fingerprinting import fingerprinting as fp

class Prediction:
    def __init__(self, receivers, reference_distance, reference_rssi, n):
        self.receivers = receivers  # receivers in the prediction area
        self.pred_dict = {}    # prediction dictionary
        self.distance_dict = {} # card_id = [("receiver_id", distance),  ... ]
        self.reference_distance = reference_distance   
        self.reference_rssi = reference_rssi    # rssi at reference_distance
        self.n = n  # coefficent that depends on environment
        self.set_fingerprinting()

    def set_fingerprinting(self):
        model_filename = 'svm_final_model.sav'
        model_features = ["msi-gt70", "raspberry-10", "erhan-e570"]
        model_classes = {0: [1,1], 1: [4.25, 2.45]}
        probability_threshold = 0.7
        self.fingerprinting = fp(model_filename, model_features, model_classes, probability_threshold)


    def combined_positioning(self, trilateration_positions, pred_dict):
        try:
            final_positions = {}
            for key, value in pred_dict.items():
                # "msi-gt70", "raspberry-10", "erhan-e570"
                ordered_rssi = []
                for receiver in self.fingerprinting.features:
                    for val in value:
                        if receiver == val[0]:
                            ordered_rssi.append(val[1])
                
                # find positions with fingerprinting
                highest_prob, highest_prob_class = self.fingerprinting.find_highest_class_prob(ordered_rssi)
                print(f'{key} = prob:{highest_prob}, class={highest_prob_class}')

                # combine trilateration and fingerprinting results
                final_x = highest_prob_class[0]*highest_prob + trilateration_positions[key][0]*(1-highest_prob)
                final_y = highest_prob_class[1]*highest_prob + trilateration_positions[key][1]*(1-highest_prob)
                final_positions[key] = [final_x, final_y]

            return final_positions
        except Exception as e:
            print(e)

    # adds new value to the prediction dictionary
    def add_new_value(self, card_id, receiver_id, rssi):
        try:
            self.pred_dict[card_id].append((receiver_id, rssi))
            return True
        except:
            self.pred_dict[card_id] = [(receiver_id, rssi)]
            return True
        return False


    def make_prediction(self):
        self.print_predictionDict()
        self.calculate_distances()
        self.print_distanceDict()
        trilateration_positions = self.trilateration(0.2)
        print("Trilateration: ", trilateration_positions)
        # final positions
        card_positions = self.combined_positioning(trilateration_positions, self.pred_dict)
        
        print("=====================   Predicted Positions   =====================")
        for key in card_positions:
            print("card_id={0}, pos=({1:.3f},{2:.3f})".format(key, card_positions[key][0], card_positions[key][1]))
            print("===================================================================")

        # show position of every card in a simple scatterplot
        #self.show_positions(card_positions, self.distance_dict, self.receivers)

        # clear dictionaries 
        self.pred_dict.clear()
        self.distance_dict.clear()
        return card_positions

    # draws a simple graph about how algorithm works        
    def show_positions(self, card_positions, distances, receivers):
        _, ax = plt.subplots()

        # limits of the plot
        plt.xlim(-4,9.25)
        plt.ylim(-4,7.45)
        
        # style the plot
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')
        ax.set_title('Card Positions', loc='center')

        # plot receivers
        for i in range(len(receivers)):
            x, y, id = receivers[i].x, receivers[i].y, receivers[i].id
            annotate_bias = 0.2
            ax.plot(x, y, 'ro')
            ax.annotate(id, (x+annotate_bias, y+annotate_bias))
     
        # draw rectangle for the room
        ax.add_patch(plt.Rectangle((0,0), 5.25, 3.45, color="green", fill=False))

        circle_colors = ['r', 'm', 'c'] # colors for every circle
        colors = ['bo', 'mo', 'co'] # colors for every end unit

        # plot cards
        for card_id in card_positions:
            j = 0
            val = card_positions[card_id]
            ax.plot(val[0], val[1], colors[j%3], label='ID:'+str(card_id)+' pos:('+str(val[0])+','+str(val[1])+')')
            ax.annotate(card_id, (val[0]+0.2, val[1]+0.2))
            
            i = 0
            for v in distances[card_id]:
                ax.add_patch(plt.Circle((v[2],v[3]), radius= v[1], color=circle_colors[i%3], fill=False))
                i += 1
            j += 1

        ax.legend()
        plt.show()
        #plt.savefig("temp.png")


    # finds position of all keys in the area
    def trilateration(self, bias):
        def inCircle(r, x, y, i, j):
            return ((i-x)**2 + (j-y)**2) <= r**2
        
        def find_single_pos(v0, v1, v2, bias, intersection_points):
            # parse distance tuples
            rec0, r0, x0, y0 = v0[:]
            rec1, r1, x1, y1 = v1[:]    
            rec2, r2, x2, y2 = v2[:]
    
            # define boundaries of intersection area
            max_x, max_y = min(14, int(r0 + x0)), min(8, int(r0 + y0))
            x_points = np.arange(0.0, max_x, 0.1)
            y_points = np.arange(0.0, max_y, 0.1)
            
            # find intersection points
            for i in x_points:
                for j in y_points:
                    if inCircle(r0, x0, y0, i, j) & \
                        inCircle(r1, x1, y1, i, j) & \
                            inCircle(r2, x2, y2, i, j):
                                intersection_points.append((i,j))
            
            # recursion in case there is no intersection
            if not intersection_points:
                r0, r1, r2 = r0+bias, r1+bias, r2+bias
                v0 = (rec0, r0, x0, y0)
                v1 = (rec1, r1, x1, y1)
                v2 = (rec2, r2, x2, y2)
                return find_single_pos(v0, v1, v2, bias, [])
            else:
                # return average as the predicted position, v0 v1 v2 for update in distance_dict
                card_x = float("{0:.3f}".format(sum([a[0] for a in intersection_points])/len(intersection_points)))
                card_y = float("{0:.3f}".format(sum([a[1] for a in intersection_points])/len(intersection_points)))
                return v0, v1, v2, (card_x, card_y)
        
        # iterate through all cards in range
        card_positions = {}
        for key in self.distance_dict:
            self.distance_dict[key][0], self.distance_dict[key][1], self.distance_dict[key][2], card_positions[key] = \
                find_single_pos(self.distance_dict[key][0], self.distance_dict[key][1], self.distance_dict[key][2], bias, [])
        
        return card_positions


    # calculates distance between transmitter and receiver, uses RSSI
    # d = d0 * 10^^( (rssi_at_d0 - rssi_calc) / (10*n) )
    def calculate_distances(self):
        n, d0, rssi_d0 = self.n, self.reference_distance, self.reference_rssi
        for key in self.pred_dict:
            for value in self.pred_dict[key]:  

                # TODO delete later - different receivers require different reference points
                if value[0] == "msi-gt70":
                    rssi_d0 = -58
                    d0 = 1
                elif value[0] == "erhan-e570":
                    rssi_d0 = -50
                    d0 = 2
                else:
                    rssi_d0 = self.reference_rssi
                    d0 = self.reference_distance

                # calculate distance
                d = float("{0:.3f}".format(d0*(10**( (rssi_d0 - value[1]) / (10*n)))))

                # get receiver coordinates
                rec_x, rec_y = 0, 0
                for rec in self.receivers:
                    if (rec.id == value[0]):
                        rec_x, rec_y = rec.x, rec.y
                        

                # add to distance dictionary
                self.add_distance(key, value[0], d, rec_x, rec_y)
        return True

    # calculates coefficent for the environment
    # n = (rssi_calculated - rssi_at_d0) / (-10 * log(d/d0)) -> log base is 10
    def _calcN(self, rssi_measured, rssi_at_d0, d, d0):
       return float("{0:.3f}".format((rssi_measured - rssi_at_d0) / (-10 * math.log10(d/d0))))

    # add new key to distance dictionary
    def add_distance(self, card_id, receiver_id, distance, rec_x, rec_y):
        try:
            self.distance_dict[card_id].append((receiver_id, distance, rec_x, rec_y))
            return True
        except:
            self.distance_dict[card_id] = [(receiver_id, distance, rec_x, rec_y)]
            return True
        return False

    def print_predictionDict(self):
        print("====================   Prediction Dictionary   ====================")
        for key in self.pred_dict:
            print("card_id = {}".format(key))
            print("===================================================================")
            print(self.pred_dict[key])
            print("\n")
        
    def print_distanceDict(self):
        print("\n=====================   Distance Dictionary   =====================")
        for key in self.distance_dict:
            print("card_id = {}".format(key))
            print("===================================================================")
            print(self.distance_dict[key])
            print("\n")
    
    def export_as_xlsx(self, filename):
        try:
            # create filename
            filename = "./" +filename+ ".xlsx"

            # create workbook object
            workbook = writer.Workbook(filename)

            # add worksheet to workbook
            worksheet = workbook.add_worksheet()

            # add labels
            worksheet.write(0, 0, "type_id")
            worksheet.write(0, 1, "receiver ID")
            worksheet.write(0, 2, "rssi")
            worksheet.write(0, 3, "battery level")
            worksheet.write(0, 4, "time")

            # write every element in dictionary to worksheet
            row = 1
            for key in self.pred_dict:
                for value in self.pred_dict[key]:
                    worksheet.write(row, 0, key)
                    for i in range(1,5):
                        worksheet.write(row, i, str(value[i-1]))
                    row += 1

            # close worksheet
            workbook.close()
            print("Last values:", end='')
            print(self.pred_dict["3_429"][-1])
            #print(self.pred_dict["3_325"][-1])
            print("Dictionary exported to " + filename + "\n")
            return True
        except:
            return False
    