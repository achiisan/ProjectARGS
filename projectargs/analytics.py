#!/usr/bin/python
import studentlist
import database
def parseRegistData():
        studentlist.loadStudentList("anon_ENLISTMENT-2")
        studentlist.loadStudentList("anon_ENLISTMENT-3.csv")
        studentlist.loadStudentList("anon_ENLISTMENT-4")
        studentlist.loadStudentList("anon_ENLISTMENT-5")

def analyzeRegistData():
    buf = database.query("SELECT * FROM studentlist where GRP is not 1 AND grp is not 0");
    #4

    filebuf_studentlist = open("args_studentlist.csv","w")
    filebuf_studentunits = open("args_studentunits.csv", "w")
    filebuf_subjectenlisted = open("args_subjectenlisted.csv","w")
    fb = open("args_ncompleteunits.csv", "w")
    filebuf_studentlist.write("stdno,name,gender,country,curriculum,scholarship,college,earned,classif,yearlevel,allowed,grp,npriority,nalternates,ncurrent\n")
    filebuf_studentunits.write("stdno,allowedunits,currentunitsenlisted\n")
    filebuf_subjectenlisted.write("stdno,schoolyear,term,course,section,units,grade,courserank,contrib\n")
    studentsCL= 0
    for entry in buf:
        for el in entry:
            filebuf_studentlist.write(str(el)+",")
        filebuf_studentlist.write("\n")
        buf2 = database.query("SELECT * FROM'"+entry[0]+"'WHERE section IS NOT ''  ")
        units = 0

        for entry2 in buf2:
            filebuf_subjectenlisted.write(entry[0]+",")
            units = units+int(entry2[4])
            for data in entry2:
                filebuf_subjectenlisted.write(data+",")
            filebuf_subjectenlisted.write("\n")
        filebuf_studentunits.write(entry[0]+","+str(entry[10])+","+str(units)+"\n")
        if entry[10] == units and units != 0:
	            fb.write(entry[0]+","+str(units)+"\n")
	            studentsCL= studentsCL + 1
    fb.write(str(studentsCL))


#parseRegistData()
analyzeRegistData()
