<img src="https://grantwinney.com/wp-content/uploads/2016/07/simon-clone-1.png" />

# Simon Clone
Here's a clone of the Simon game from the 80's.

[Read more about the setup here](https://grantwinney.com/creating-a-simon-game-clone-on-the-raspberry-pi/), and then [check out everything I'm doing with the Pi](https://grantwinney.com/tag/52-weeks-of-pi/).

## To Run

Run the Simon.py file.

I uploaded a [demo](https://youtu.be/cpj_cc2ZkEU) if you're interested in seeing it work.

## Notes:

* Leave `use_sounds = True` to hear the sounds, but set it to `False` for a more "even" gameplay.

* Click those buttons firmly... a lot of them are cheap and will register multiple clicks when you only clicked it once. I set a "bouncetime" that should counteract that, but still...

## Resources:

* <a href="http://www.cl.cam.ac.uk/projects/raspberrypi/sonicpi/media/sonic-pi-cheatsheet.pdf">Sonic Pi Cheat Sheet</a>
* <a href="https://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/">RPi.GPIO Usage Examples</a>
* <a href="https://gist.github.com/rbnpi/2c6d2da3246f64f4d97e">Tuning Sonic Pi for best performance</a>
