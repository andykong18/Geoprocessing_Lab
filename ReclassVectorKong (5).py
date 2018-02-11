
# coding: utf-8

# In[9]:

#importing Arcpy and setting the enviroment
import arcpy
arcpy.env.overwriteOutput = True


# In[15]:

#imputting the shapefile
original = arcpy.GetParameterAsText(0)

#infield parameter
infield = arcpy.GetParameterAsText(1)

#outfield parameter
outfield = arcpy.GetParameterAsText(2)

#output shapefile
output = arcpy.GetParameterAsText(3)

#dataset table used to reclassify the population density
Reclasstable= arcpy.GetParameterAsText(4)

#set value that are out of bounds
notfoundvalue = arcpy.GetParameterAsText(5)



# In[12]:

#copy the original shape file into a new one that will store the reclassified values.
arcpy.CopyFeatures_management(original,output)
arcpy.AddField_management(output, str(outfield))

cursor = arcpy.da.UpdateCursor(output,[infield,outfield])
for row in cursor:
    cursor1 = arcpy.da.SearchCursor(Reclasstable,["lowerbound","upperbound","value"])
    boolean = False
    for row1 in cursor1:
        if(row[0]<=row1[1] and row[0]>=row1[0]):
            row[1]=row1[2]
            cursor.updateRow(row)
            boolean = True
            break
    if not boolean:
        row[1] = notfoundvalue
        cursor.updateRow(row)
del cursor1
del cursor

