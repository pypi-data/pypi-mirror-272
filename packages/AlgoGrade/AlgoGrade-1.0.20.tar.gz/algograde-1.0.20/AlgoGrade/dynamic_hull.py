from __future__ import annotations
from functools import partial
from typing import ClassVar, Optional, Union
from PyCompGeomAlgorithms.core import PathDirection
from PyCompGeomAlgorithms.dynamic_hull import upper_dynamic_hull, DynamicHullNode, DynamicHullTree, SubhullNode, SubhullThreadedBinTree
from .adapters import pycga_to_pydantic, pydantic_to_pycga, PointPydanticAdapter, BinTreeNodePydanticAdapter, BinTreePydanticAdapter, ThreadedBinTreeNodePydanticAdapter, ThreadedBinTreePydanticAdapter
from .core import Task, Grader, Answers, Mistake
from .parsers import PointListAndTargetPointGivenJSONParser


class DynamicHullGrader(Grader):
    @classmethod
    def grade_methods(cls):
        return [
            cls.grade_iterable,
            partial(
                cls.grade_bin_tree,
                grade_item_method=lambda a, c, gp: cls.grade_iterable(
                    (a.left_supporting, a.right_supporting),
                    (c.left_supporting, c.right_supporting),
                    gp
                )
            ),
            cls.grade_omitted_points,
            partial(
                cls.grade_bin_tree,
                grade_item_method=lambda a, c, gp: cls.grade_iterable(
                    [n.point for n in a.subhull.traverse_inorder()],
                    [n.point for n in c.subhull.traverse_inorder()],
                    gp
                )
            ),
            partial(
                cls.grade_bin_tree,
                grade_item_method=lambda a, c, gp: cls.grade_object(a.left_supporting_index, c.left_supporting_index, gp)
            ),
            partial(
                cls.grade_bin_tree,
                grade_item_method=lambda a, c, gp: cls.grade_iterable(
                    a.optimized_subhull.traverse_inorder(),
                    c.optimized_subhull.traverse_inorder(),
                    gp
                )
            ),
            cls.grade_iterable,
            partial(cls.grade_iterable, grade_item_method=[cls.grade_bin_tree, cls.grade_iterable])
        ]
    
    @classmethod
    def grade_omitted_points(cls, answer, correct_answer, scorings):
        def grade_item_method(a, c, gp):
            if not a.is_leaf:
                correct_subhull = {node.point for node in c.subhull.traverse_inorder()}
                correct_left_subhull = {node.point for node in c.left.subhull.traverse_inorder()}
                correct_right_subhull = {node.point for node in c.right.subhull.traverse_inorder()}
                correct_omitted_points = (correct_left_subhull | correct_right_subhull) - correct_subhull

                subhull = {node.point for node in a.subhull.traverse_inorder()}
                if non_omitted_points := subhull & correct_omitted_points:
                    return [Mistake(gp)] * len(non_omitted_points)

            return []
        
        return cls.grade_bin_tree(answer, correct_answer, scorings, grade_item_method)


class DynamicHullNodePydanticAdapter(BinTreeNodePydanticAdapter):
    regular_class: ClassVar[type] = DynamicHullNode
    data: PointPydanticAdapter
    left: Optional[DynamicHullNodePydanticAdapter] = None
    right: Optional[DynamicHullNodePydanticAdapter] = None
    subhull_points: list[PointPydanticAdapter]
    optimized_subhull_points: Optional[list[PointPydanticAdapter]] = None
    left_supporting_index: int = 0
    left_supporting: PointPydanticAdapter
    right_supporting: PointPydanticAdapter

    @classmethod
    def from_regular_object(cls, obj: DynamicHullNode, **kwargs):
        return super().from_regular_object(
            obj,
            subhull_points=pycga_to_pydantic([node.point for node in obj.subhull.traverse_inorder()]),
            optimized_subhull_points=pycga_to_pydantic([node.point for node in obj.optimized_subhull.traverse_inorder()]),
            left_supporting_index=obj.left_supporting_index,
            left_supporting=pycga_to_pydantic(obj.left_supporting),
            right_supporting=pycga_to_pydantic(obj.right_supporting),
            **kwargs
        )


class DynamicHullTreePydanticAdapter(BinTreePydanticAdapter):
    regular_class: ClassVar[type] = DynamicHullTree
    root: DynamicHullNodePydanticAdapter

    @classmethod
    def from_regular_object(cls, obj: DynamicHullTree, **kwargs):
        return super().from_regular_object(obj, **kwargs)


class SubhullNodePydanticAdapter(ThreadedBinTreeNodePydanticAdapter):
    regular_class: ClassVar[type] = SubhullNode
    data: PointPydanticAdapter
    left: Optional[SubhullNodePydanticAdapter] = None
    right: Optional[SubhullNodePydanticAdapter] = None
    prev: Optional[Union[SubhullNodePydanticAdapter, int]] = None
    next: Optional[Union[SubhullNodePydanticAdapter, int]] = None

    @classmethod
    def from_regular_object(cls, obj: SubhullNode, **kwargs):
        return super().from_regular_object(obj, **kwargs)


class SubhullThreadedBinTreePydanticAdapter(ThreadedBinTreePydanticAdapter):
    regular_class: ClassVar[type] = SubhullThreadedBinTree
    root: SubhullNodePydanticAdapter

    @classmethod
    def from_regular_object(cls, obj: SubhullThreadedBinTree, **kwargs):
        return super().from_regular_object(obj, **kwargs)


class DynamicHullAnswers(Answers):
    tree: DynamicHullTreePydanticAdapter
    path: list[PathDirection]
    modified_tree: DynamicHullTreePydanticAdapter
    hull: list[PointPydanticAdapter]

    @classmethod
    def from_iterable(cls, iterable):
        _, tree, _, _, _, _, path, (modified_tree, hull), *rest = iterable
        return cls(tree=tree, path=path, modified_tree=modified_tree, hull=hull)
    
    def to_pydantic_list(self):
        return [
            self.tree.leaves_inorder(), self.tree, self.tree, self.tree, self.tree,
            self.tree, self.path, (self.modified_tree, self.hull)
        ]


class DynamicHullTask(Task):
    algorithm = upper_dynamic_hull
    grader_class = DynamicHullGrader
    answers_class = DynamicHullAnswers
    given_parser_class = PointListAndTargetPointGivenJSONParser
