class Logic_Settings:
    #LCD
    cols = 20
    rows = 4
    charmap = 'A00'
    i2c_expander = 'PCF8574'
    address = 0x27 
    port = 1

    #MIDI
    midi_port = 'Microsoft GS Wavetable Synth 0'

    #Directories
    dev_dir = './dev/'
    usb_dir = './usb/'
    onboard_dir = './onboard/'