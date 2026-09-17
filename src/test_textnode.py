import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("test", TextType.IMAGE, "asd")
        node4 = TextNode("test", TextType.ITALIC, "asd")
        self.assertNotEqual(node3, node4)

        node5 = TextNode("test", TextType.IMAGE, "asd")
        node6 = TextNode("est", TextType.IMAGE, "asd")
        self.assertNotEqual(node5,node6)

        node5 = TextNode("test", TextType.IMAGE, "asd")
        node6 = TextNode("est", TextType.IMAGE, "asd")
        self.assertNotEqual(node5,node6)


if __name__ == "__main__":
    unittest.main()