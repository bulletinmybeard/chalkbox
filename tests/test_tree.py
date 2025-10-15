from chalkbox.components.tree import Tree


class TestTree:
    """Tests for Tree component."""

    def test_tree_creation(self):
        """Test basic tree creation."""
        tree = Tree("Root")
        assert tree is not None

    def test_tree_add_branch(self):
        """Test adding a branch to tree."""
        tree = Tree("Root")
        branch = tree.add("Branch 1")
        assert branch is not None
        assert isinstance(branch, Tree)

    def test_tree_nested_branches(self):
        """Test nested branches."""
        tree = Tree("Root")
        branch1 = tree.add("Branch 1")
        branch2 = branch1.add("Nested Branch")
        assert branch2 is not None

    def test_tree_add_branch_with_list(self):
        """Test add_branch with list of items."""
        tree = Tree("Root")
        items = ["Item 1", "Item 2", "Item 3"]
        branch = tree.add_branch("Branch", items)
        assert branch is not None

    def test_tree_add_branch_with_dict(self):
        """Test add_branch with dictionary."""
        tree = Tree("Root")
        items = {"key1": "value1", "key2": "value2"}
        branch = tree.add_branch("Config", items)
        assert branch is not None

    def test_tree_from_dict(self):
        """Test creating tree from dictionary."""
        data = {"name": "Project", "version": "1.0", "config": {"debug": True}}
        tree = Tree.from_dict(data, root_label="Settings")
        assert tree is not None

    def test_tree_from_dict_with_lists(self):
        """Test from_dict with lists."""
        data = {"items": ["item1", "item2"], "nested": [{"key": "value"}]}
        tree = Tree.from_dict(data)
        assert tree is not None

    def test_tree_simple_factory(self):
        """Test simple factory method."""
        items = ["Task 1", "Task 2", "Task 3"]
        tree = Tree.simple("TODO List", items)
        assert tree is not None

    def test_tree_expanded_param(self):
        """Test tree with expanded parameter."""
        tree = Tree("Root", expanded=False)
        assert tree is not None

    def test_tree_render(self):
        """Test tree renders without error."""
        tree = Tree("Root")
        tree.add("Branch 1")
        tree.add("Branch 2")
        rendered = tree.__rich__()
        assert rendered is not None
