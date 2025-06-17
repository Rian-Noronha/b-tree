#include <iostream>
using namespace std;

class BTreeNode {
public:
    int *keys;
    int t;
    BTreeNode **children;
    int n;
    bool leaf;

    BTreeNode(int _t, bool _leaf) {
        t = _t;
        leaf = _leaf;
        keys = new int[2 * t - 1];
        children = new BTreeNode *[2 * t];
        n = 0;
    }

    void traverse() {
        int i;
        for (i = 0; i < n; i++) {
            if (!leaf) {
                children[i]->traverse();
            }
            cout << " " << keys[i];
        }
        if (!leaf) {
            children[i]->traverse();
        }
    }

    BTreeNode *search(int k) {
        int i = 0;
        while (i < n && k > keys[i]) {
            i++;
        }
        if (i < n && keys[i] == k) {
            return this;
        }
        if (leaf) {
            return nullptr;
        }
        return children[i]->search(k);
    }

    void insertNonFull(int k);
    void splitChild(int i, BTreeNode *y);
};

class BTree {
public:
    BTreeNode *root;
    int t;

    BTree(int _t) {
        root = nullptr;
        t = _t;
    }

    void traverse() {
        if (root != nullptr) {
            root->traverse();
        }
    }

    BTreeNode *search(int k) {
        return (root == nullptr) ? nullptr : root->search(k);
    }

    void insert(int k);
};

void BTreeNode::insertNonFull(int k) {
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
        if (children[i]->n == 2 * t - 1) {
            splitChild(i, children[i]);
            if (keys[i] < k) {
                i++;
            }
        }
        children[i]->insertNonFull(k);
    }
}

void BTreeNode::splitChild(int i, BTreeNode *y) {
    BTreeNode *z = new BTreeNode(y->t, y->leaf);
    z->n = t - 1;
    for (int j = 0; j < t - 1; j++) {
        z->keys[j] = y->keys[j + t];
    }
    if (!y->leaf) {
        for (int j = 0; j < t; j++) {
            z->children[j] = y->children[j + t];
        }
    }
    y->n = t - 1;
    for (int j = n; j >= i + 1; j--) {
        children[j + 1] = children[j];
    }
    children[i + 1] = z;
    for (int j = n - 1; j >= i; j--) {
        keys[j + 1] = keys[j];
    }
    keys[i] = y->keys[t - 1];
    n++;
}

void BTree::insert(int k) {
    if (root == nullptr) {
        root = new BTreeNode(t, true);
        root->keys[0] = k;
        root->n = 1;
    } else {
        if (root->n == 2 * t - 1) {
            BTreeNode *s = new BTreeNode(t, false);
            s->children[0] = root;
            s->splitChild(0, root);
            int i = 0;
            if (s->keys[0] < k) {
                i++;
            }
            s->children[i]->insertNonFull(k);
            root = s;
        } else {
            root->insertNonFull(k);
        }
    }
}

int main() {
    BTree t(3);
    int keys[] = {10, 20, 5, 6, 12, 30, 7, 17};
    for (int i = 0; i < sizeof(keys) / sizeof(keys[0]); i++) {
        t.insert(keys[i]);
    }

    cout << "Traversal of the constructed B-tree is:";
    t.traverse();
    cout << endl;

    int k = 6;
    (t.search(k) != nullptr) ? cout << "Present\n" : cout << "Not Present\n";

    k = 15;
    (t.search(k) != nullptr) ? cout << "Present\n" : cout << "Not Present\n";

    return 0;
}