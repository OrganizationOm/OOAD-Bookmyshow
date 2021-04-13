import json

# data={"Inox Multiplex" : ["10:00 am","12:00 pm", "2:00 pm", "4:00 pm" , "6:00 pm", "8:00 pm", "10:00 pm"], "PVR Whitefield": ["10:15 am","12:30 pm", "2:45 pm", "4:15 pm" , "6:30 pm", "8:35 pm", "10:40 pm"], "Fame Cinemas" : ["9:15 am","11:30 pm", "1:45 pm", "2:15 pm"], "VR Mall" : [ "6:30 pm", "8:35 pm", "10:40 pm"]}
# f = open('movie_file.json')
# data=json.load(f)

# data["Avengers"]={"name":"Avengers","rating":"5","description":"After half of all life is snapped away by Thanos, the Avengers are left scattered and divided. Now with a way to reverse the damage, the Avengers and their allies must assemble once more and learn to put differences aside in order to work together and set things right. Along the way, the Avengers realize that sacrifices must be made as they prepare for the ultimate final showdown with Thanos, which will result in the heroes fighting the biggest battle they have ever faced."}


data= {"Om719" : []}
with open("user_history_file.json", "w") as write_file:
    json.dump(data, write_file)