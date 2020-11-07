from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title('Music player')
root.iconbitmap('./icon.png')
root.geometry("500x350")

#initilize pygame mixer
pygame.mixer.init()

# grabe song length and time
def play_time():
    current_time = pygame.mixer.music.get_pos()/1000
    # convert to time formate
    converted_crrent_time = time.strftime('%M:%S',time.gmtime(current_time))

    # get the crrent plaing song
    current_song = song_box.curselection()
    # Grab song title from songlist
    song = song_box.get(ACTIVE)
    # add directory structure and mp3 to song title
    song = f'C:/Users/Sachin/Desktop/Music/{song}.mp3'
    # get song length with mutagen
    #load song ith mutagen
    song_mut = MP3(song)
    #get song length
    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))


    starus_bar.config(text=f'Time Elapsed: {converted_crrent_time} of {converted_song_length}  ')
    # uupdate time
    starus_bar.after(1000,play_time)

#add song function
def add_song():
    song = filedialog.askopenfilename(initialdir='Music player',title="Chose A Song",filetype=(("mp3 Files","*.mp3"),))

    #strip out the directory info and .mp3 extention from the s
    song = song.replace("C:/Users/Sachin/Desktop/Music/","")
    song = song.replace(".mp3","")

    song_box.insert(END,song)

# Add many songs
def add_many_song():
    songs = filedialog.askopenfilenames(initialdir='Music player', title="Chose A Song",filetype=(("mp3 Files", "*.mp3"),))

    # Loop thrue songs to playlist
    for song in songs:
        song = song.replace("C:/Users/Sachin/Desktop/Music/", "")
        song = song.replace(".mp3", "")
        # insert into playlist
        song_box.insert(END, song)

#play selecting song
def play():
    song = song_box.get(ACTIVE)
    song = f'C:/Users/Sachin/Desktop/Music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #call the play time function to get song length
    play_time()
#stop playing current song
def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    starus_bar.selection_clear(text=0)

# delete a song
def delete_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()
    #clear status bar
    starus_bar.config(text='')

#delete all songs
def delete_all_songs():
    song_box.delete(0,END)
    pygame.mixer.music.stop()

#crete global pause button
global paused
paused = False

#pause and unpause
def pause(is_pused):
    global paused
    paused = is_pused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

#play the next song
def next_button():
    #get the crrent song number
    next_one = song_box.curselection()
    #add one to the current song number
    next_one = next_one[0]+1
    # Grab song title from songlist
    song = song_box.get(next_one)
    # add directory structure and mp3 to song title
    song = f'C:/Users/Sachin/Desktop/Music/{song}.mp3'
    #load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #clear active bar in plalist box
    song_box.selection_clear(0,END)
    #activate new song
    song_box.activate(next_one)
    #set active bar for next song
    song_box.selection_set(next_one,last=None)

#previos song
def previos_song():
    # get the crrent song number
    next_one = song_box.curselection()
    # add one to the current song number
    next_one = next_one[0] - 1
    # Grab song title from songlist
    song = song_box.get(next_one)
    # add directory structure and mp3 to song title
    song = f'C:/Users/Sachin/Desktop/Music/{song}.mp3'
    # load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # clear active bar in plalist box
    song_box.selection_clear(0, END)
    # activate new song
    song_box.activate(next_one)
    # set active bar for next song
    song_box.selection_set(next_one, last=None)


#create plalist box
song_box = Listbox(root,bg="black",fg="green",width=60,selectbackground="gray",selectforeground="black")


song_box.pack(pady=20)

#create player control button images
back_btn_img = PhotoImage(file='prev.png')
forward_btn_img = PhotoImage(file='next.png')
play_btn_img = PhotoImage(file='play1.png')
pause_btn_img = PhotoImage(file='pause.png')
stop_btn_img = PhotoImage(file='stop.png')

#create player control frame
control_frame = Frame(root)
control_frame.pack()

#create player control buttons
back_button = Button(control_frame,image=back_btn_img, borderwidth=0,command=previos_song)
forward_button = Button(control_frame,image=forward_btn_img, borderwidth=0,command = next_button)
paly_button = Button(control_frame,image=play_btn_img, borderwidth=0,command=play)
pause_button = Button(control_frame,image=pause_btn_img, borderwidth=0,command=lambda : pause(paused))
stop_button = Button(control_frame,image=stop_btn_img, borderwidth=0,command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
paly_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

#create menu
my_menu = Menu(root)
root.config(menu=my_menu)

#add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs",menu=add_song_menu)
add_song_menu.add_cascade(label="Add one song to playlist",command=add_song)

# add many song for play
add_song_menu.add_cascade(label="Add many song to playlist",command=add_many_song)

# Create delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs",menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist",command=delete_song)
remove_song_menu.add_command(label="Delete All Song From Playlist",command=delete_all_songs)

# create status bar
starus_bar = Label(root,text='',bd=1,relief=GROOVE,anchor=E)
starus_bar.pack(fill=X,side=BOTTOM,ipady=2)

root.mainloop()
