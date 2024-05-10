# coding=utf-8

from flutter_gen.generate.generate_color_cmd import GenerateColorCommand
from flutter_gen.generate.generate_font_cmd import GenerateFontCommand
from flutter_gen.generate.generate_r_cmd import GenerateRCommand
from flutter_gen.generate.generate_repo_cmd import GenerateRepoCommand
from flutter_gen.generate.generate_router_cmd import GenerateRouterCommand
from flutter_gen.generate.generate_image_cmd import GenerateImageCommand
from flutter_gen.generate.generate_localization_cmd import GenerateLocalizationCommand
from flutter_gen.generate.generate_object_mapper_cmd import GenerateObjectMapperCommand
from flutter_gen.utils.debounce import debounce
from flutter_gen.utils.print import print_info
from ..core.command import Command
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import multiprocessing
import time
import os


class RunCommand(Command):
    def __init__(self):
        super(RunCommand, self).__init__()

    def build_runner(self):
        os.system("flutter pub run build_runner build --delete-conflicting-outputs")

    def createFile(self, path):
        if not os.path.isfile(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            print_info("Creating %s completed" % (path))
            with open(path, "w"):
                pass

    def run(self):
        # Gen file
        self.createFile("assets/color/colors.txt")
        # Gen all
        # GenerateImageCommand().run()
        # GenerateLocalizationCommand().run()
        # GenerateColorCommand().run()
        GenerateRCommand().run()
        # GenerateObjectMapperCommand().run()
        GenerateRouterCommand().run()
        GenerateFontCommand().run()
        GenerateRepoCommand().run()
        self.build_runner()
