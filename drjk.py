import csv
import sys

def txt_time_real(time):
    hours = int(time[:time.index(':')])
    minutes = int(time[time.index(':')+1:])
    return hours*60 + minutes

def real_time_txt(mns):
    hour = mns // 60
    minutes = mns % 60

    if minutes < 10:
        res = "0"+str(minutes) 
    else:
        res = f"{minutes}"

    return f"{hour}:{res}"



def solve(file_name):
    times = []


    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        # Skip header row
        next(csv_reader)

        
        for row in csv_reader:
            participant, start_time, end_time = row
            
            # Check if there is no participant name (split by commas gives an empty string)
            if not participant:
                times[-1].append([txt_time_real(start_time), txt_time_real(end_time)])
            else:
                times.append([[txt_time_real(start_time), txt_time_real(end_time)]])


    for i in times:
        i.sort(key=lambda x: x[0])

    not_poss_times = []
    for c,i in enumerate(times):
        last_time = 9 * 60
        for j in i:
            if last_time < j[0]:
                not_poss_times.append([last_time, j[0]])
            last_time = max(last_time, j[1])
        
        if i[-1][-1] < 17*60:
            not_poss_times.append([i[-1][-1], 17*60])


    not_poss_times.sort()

    res = [[9*60, 9*60]]

    for i in not_poss_times:
        if res[-1][0] == i[0]:
            res[-1] = i
        elif res[-1][-1] > i[0]:
            res[-1][-1] = max(i[1], res[-1][-1])
        else:
            res.append(i)
        
    res.append([17*60,17*60])

    dur = 0

    for i in range(1, len(res)):
        if dur < res[i][0] - res[i-1][1]:
            dur = res[i][0] - res[i-1][1]
            out = [res[i-1][1], res[i][0]]

    if dur <= 0:
        return("None", dur)
    else:
        return(real_time_txt(out[0]), dur)
    
if __name__ == "__main__":
    filename = sys.argv[1]
    solve(filename)