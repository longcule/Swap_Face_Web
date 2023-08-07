#!/usr/bin/env python3

from roop import core
import roop.globals
if __name__ == '__main__':
    roop.globals.target_path = "/home/longcule/Music/roop-main/results/output_full2.jpg"
    roop.globals.source_path = "/home/longcule/Music/roop-main/jake-nackos-IF9-TK5-Uy-KI-unsplash.jpg"
    roop.globals.output_path = "/home/longcule/Music/roop-main/out1112.png"
    core.run()