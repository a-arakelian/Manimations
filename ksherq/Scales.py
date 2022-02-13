from manim import *
import numpy as np
import sys

sys.path.append('../')

from Objects.Objects import *


class Scales(Scene):
    def construct(self):

        self.left_part_list_of_str = ['apple', 'apple', 'apple', 'apple',]
        self.right_part_list_of_str = ['apple', 'apple', 'kb_7_kg', 'kb_13_kg']

        self.left_part_apples = [0, 1, 2, 3]
        self.right_part_apples = [0, 1]

        self.add_objects(self.left_part_list_of_str, self.right_part_list_of_str)
        # kettlebell = Weight(5)
        # # self.play(Create(kettlebell.weight))


        # new_kbs = self.split_kettlebell_into_several(kettlebell, [3, 1, 2], play_animation=False)
        # self.combine_kettlebells(new_kbs)


    @staticmethod
    def convert_list_of_items_to_list_of_mobjects(items):
        mobjs = []
        for i in items:
            if i == "apple":
                mobjs.append(SVGMobject('apple.svg').scale(0.4).set_color(GREEN))
            if i.startswith('kb'):
                kb_weight = int(i.split('_')[1])
                mobjs.append(Weight(kb_weight))
        return mobjs

    def allign_mobjs_next_to_eact_other(self,mobjs):
        for i in range(len(mobjs)-1):
            if self.is_weight(mobjs[i+1]):
                if self.is_weight(mobjs[i]):
                    mobjs[i+1].weight.next_to(mobjs[i].weight)
                else:
                    mobjs[i+1].weight.next_to(mobjs[i])
            else:
                if self.is_weight(mobjs[i]):
                    mobjs[i+1].next_to(mobjs[i].weight)
                else:
                    mobjs[i+1].next_to(mobjs[i])


    @staticmethod
    def is_weight(mobj):
        return "Weight" in str(mobj)

    def add_objects(self, left_part, right_part):
        left_part = self.convert_list_of_items_to_list_of_mobjects(left_part)
        right_part = self.convert_list_of_items_to_list_of_mobjects(right_part)

        if self.is_weight(left_part[0]):
            left_part[0].weight = left_part[0].weight.shift(LEFT * 4)
        else:
            left_part[0] = left_part[0].shift(LEFT * 4)

        if self.is_weight(right_part[0]):
            right_part[0].weight = right_part[0].weight.shift(RIGHT)
        else:
            right_part[0] = right_part[0].shift(RIGHT)






        self.allign_mobjs_next_to_eact_other(left_part)
        self.allign_mobjs_next_to_eact_other(right_part)

        self.left_part = left_part 
        self.right_part = right_part

        # print(all_items[0].weight)
        # self.play(Create(all_items[0].weight))


        # print(all_items[1])
        # self.play(Create(all_items[1].shift(RIGHT*3)))

        for i in left_part + right_part:
            print(str(i))
            if "Weight" in str(i):
                print(i)
                self.play(Create(i.weight), run_time=0.75)#.shift(RIGHT*i)))
            else:
                self.play(Create(i), run_time=0.75)#.shift(RIGHT*1)))

        big_kettlebell = self.combine_kettlebells([right_part[-2], right_part[-1]], play_animation=True)
        # self.split_kettlebell_into_several(big_kettlebell, [3,3,4])
        self.remove_obj()



    def remove_obj(self, objs='2_apple', part='left'):
        num = int(objs.split('_')[0])
        
        print(self.left_part)
        print(self.left_part[self.left_part_apples[0]])

        for i in range(num):
            self.play(FadeOut(self.left_part[self.left_part_apples[i]]))
            self.play(FadeOut(self.right_part[self.right_part_apples[i]]))
        print('removes')
            
        # objs = [i for i, j in enumerate(self.left_part_list_of_str) if j == '']









    @staticmethod
    def kettlebell_weights_vgroup(kettlebells):
        return VGroup(*[i.weight for i in kettlebells])

    def split_kettlebell_into_several(self, kettlebell, new_weights, play_animation=True):
        if kettlebell.kg != sum(new_weights):
            raise Exception(f"You can't split {kettlebell.kg} kettlebell into kettlebells with weights {new_weights}")


        new_kettlebells = [Weight(w) for w in new_weights]

        for i in range(len(new_kettlebells)-1):
            new_kettlebells[i+1].weight.next_to(new_kettlebells[i].weight, RIGHT)


        all_weights = self.kettlebell_weights_vgroup(new_kettlebells)

        self.wait(1)
        all_weights.move_to(kettlebell.weight.get_center() + np.array([1,2,0]))

        if play_animation:
            self.play(Transform(kettlebell.weight, all_weights))
            # self.remove(kettlebell.weight)

        return new_kettlebells


    def combine_kettlebells(self, kettlebells, play_animation=True):
        big_kettlebell_weight = sum([i.kg for i in kettlebells])
        big_kettlebell_position = np.mean([i.weight.get_center() for i in kettlebells], axis=0)
        print('New_kettlebell pos', big_kettlebell_position)
        big_kettlebell = Weight(big_kettlebell_weight)

        big_kettlebell.weight.move_to(big_kettlebell_position)

        if play_animation:
            self.play(Transform(VGroup(*[i.weight for i in kettlebells]), big_kettlebell.weight))
        return big_kettlebell
