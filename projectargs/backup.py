if currId in subjecttree.subjecttrees:
			#get bucket
			st = subjecttree.subjecttrees[currId]
			bucket = st.it_buckets[st.bucketcounter]

			enlistcompleted = False

			stud = ScheduleMap(student[0])
			print("ENLIST = "+student[0])
			
			while  enlistcompleted == False:
				print("Get bucket")
				for item in bucket.items():
					print(item.data.classinfo)
					bucketFailed = False
					if item.data.classinfo[0] in courses_list or bucketFailed == False:
						if mongo_database.getSlot(item.data.classinfo[0]+"-"+item.data.classinfo[1])["nModified"] == 1:
							stud.schedule.add(item)
						else:
							print("Invalid line")
							bucketFailed = True
				if bucketFailed == True:
					st.bucketcounter = st.bucketcounter + 1
					if bucketindex < len(st.it_buckets):
						bucket = st.it_buckets[st.bucketcounter]
						stud = ScheduleMap(student[0])
				else:
					enlistcompleted = True


				schedulemap.schedules[student[0]] = stud

	printToFileSchedule()