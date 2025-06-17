class BTreeNode {
    int[] keys;
    int t;
    BTreeNode[] children;
    int n;
    boolean leaf;

    public BTreeNode(int t, boolean leaf) {
        this.t = t;
        this.leaf = leaf;
        this.keys = new int[2 * t - 1];
        this.children = new BTreeNode[2 * t];
        this.n = 0;
    }

    public void traverse() {
        int i;
        for (i = 0; i < n; i++) {
            if (!leaf) {
                children[i].traverse();
            }
            System.out.print(" " + keys[i]);
        }
        if (!leaf) {
            children[i].traverse();
        }
    }

    public BTreeNode search(int k) {
        int i = 0;
        while (i < n && k > keys[i]) {
            i++;
        }
        if (i < n && keys[i] == k) {
            return this;
        }
        if (leaf) {
            return null;
        }
        return children[i].search(k);
    }

    public void insertNonFull(int k);
    public void splitChild(int i, BTreeNode y);
}

class BTree {
    BTreeNode root;
    int t;

    public BTree(int t) {
        this.root = null;
        this.t = t;
    }

    public void traverse() {
        if (root != null) {
            root.traverse();
        }
    }

    public BTreeNode search(int k) {
        return (root == null) ? null : root.search(k);
    }

    public void insert(int k);
}

void BTreeNode.insertNonFull(int k) {
    int i = n - 1;
    if (leaf) {
        while (i >= 0 && keys[i] > k) {
            keys[i + 1] = keys[i];
            i--;
        }
        keys[i + 1] = k;
        n++;
    } else {
        while (i >= 0 && keys[i] > k) {
            i--;
        }
        i++;
        if (children[i].n == 2 * t - 1) {
            splitChild(i, children[i]);
            if (keys[i] < k) {
                i++;
            }
        }
        children[i].insertNonFull(k);
    }
}

void BTreeNode.splitChild(int i, BTreeNode y) {
    BTreeNode z = new BTreeNode(y.t, y.leaf);
    z.n = t - 1;
    for (int j = 0; j < t - 1; j++) {
        z.keys[j] = y.keys[j + t];
    }
    if (!y.leaf) {
        for (int j = 0; j < t; j++) {
            z.children[j] = y.children[j + t];
        }
    }
    y.n = t - 1;
    for (int j = n; j >= i + 1; j--) {
        children[j + 1] = children[j];
    }
    children[i + 1] = z;
    for (int j = n - 1; j >= i; j--) {
        keys[j + 1] = keys[j];
    }
    keys[i] = y.keys[t - 1];
    n++;
}

void BTree.insert(int k) {
    if (root == null) {
        root = new BTreeNode(t, true);
        root.keys[0] = k;
        root.n = 1;
    } else {
        if (root.n == 2 * t - 1) {
            BTreeNode s = new BTreeNode(t, false);
            s.children[0] = root;
            s.splitChild(0, root);
            int i = 0;
            if (s.keys[0] < k) {
                i++;
            }
            s.children[i].insertNonFull(k);
            root = s;
        } else {
            root.insertNonFull(k);
        }
    }
}

public class Main {
    public static void main(String[] args) {
        BTree t = new BTree(3);
        int keys[] = {10, 20, 5, 6, 12, 30, 7, 17};
        for (int key : keys) {
            t.insert(key);
        }

        System.out.println("Traversal of the constructed B-tree is:");
        t.traverse();
        System.out.println();

        int k = 6;
        System.out.println(t.search(k) != null ? "Present" : "Not Present");

        k = 15;
        System.out.println(t.search(k) != null ? "Present" : "Not Present");
    }
}