# oliver-spaceship-two


Switches   Switches
(Ard.1)    (Ard.2)
    \\     //
     \\   //
       | |
       | |  Serial Lines:  JSON messages from switches are read from here
       | |  
        V             
  SerialProcessor: Takes messages from the serial lines, and passes to a state controller
       | |         Converts JSON message to audio queue control message (dict)       
       | |         Will pass the message to a state controller for
       | |
       | |  audiocontroller.audio_queue
       | |  
        V             
  AudioController:  Listens to incoming messages from the serial processor,
                    and plays the relevant sound.
