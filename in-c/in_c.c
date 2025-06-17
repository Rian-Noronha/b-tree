#include <stdio.h>
#include <stdlib.h>

typedef struct BTreeNode {
    int *keys;
    int t;
    struct BTreeNode **children;
    int n;
    int leaf;
} BTreeNode;

BTreeNode *createNode(int t, int leaf) {
    BTreeNode *node = (BTreeNode *)malloc(sizeof(BTreeNode));
    node->t = t;
    node->leaf = leaf;
    node->keys = (int *)malloc((2 * t - 1) * sizeof(int));
    node->children = (BTreeNode **)malloc(2 * t * sizeof(BTreeNode *));
    node->n = 0;
    return node;
}

void traverse(BTreeNode *root) {
    if (root != NULL) {
        int i;
        for (i = 0; i < root->n; i++) {
            if (!root->leaf) {
                traverse(root->children[i]);
            }
            printf(" %d", root->keys[i]);
        }
        if (!root->leaf) {
            traverse(root->children[i]);
        }
    }
}

BTreeNode *search(BTreeNode *root, int k) {
    int i = 0;
    while (i < root->n && k > root->keys[i]) {
        i++;
    }
    if (i < root->n && root->keys[i] == k) {
        return root;
    }
    if (root->leaf) {
        return NULL;
    }
    return search(root->children[i], k);
}

void insertNonFull(BTreeNode *node, int k) {
    int i = node->n - 1;
    if (node->leaf) {
        while (i >= 0 && node->keys[i] > k) {
            node->keys[i + 1] = node->keys[i];
            i--;
        }
        node->keys[i + 1] = k;
        node->n++;
    } else {
        while (i >= 0 && node->keys[i] > k) {
            i--;
        }
        i++;
        if (node->children[i]->n == 2 * node->t - 1) {
            splitChild(node, i);
            if (node->keys[i] < k) {
                i++;
            }
        }
        insertNonFull(node->children[i], k);
    }
}

void splitChild(BTreeNode *node, int i) {
    int t = node->t;
    BTreeNode *z = createNode(t, node->children[i]->leaf);
    BTreeNode *y = node->children[i];
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
    for (int j = node->n; j >= i + 1; j--) {
        node->children[j + 1] = node->children[j];
    }
    node->children[i + 1] = z;
    for (int j = node->n - 1; j >= i; j--) {
        node->keys[j + 1] = node->keys[j];
    }
    node->keys[i] = y->keys[t - 1];
    node->n++;
}

void insert(BTreeNode **root, int k, int t) {
    if (*root == NULL) {
        *root = createNode(t, 1);
        (*root)->keys[0] = k;
        (*root)->n = 1;
    } else {
        if ((*root)->n == 2 * t - 1) {
            BTreeNode *s = createNode(t, 0);
            s->children[0] = *root;
            splitChild(s, 0);
            int i = 0;
            if (s->keys[0] < k) {
                i++;
            }
            insertNonFull(s->children[i], k);
            *root = s;
        } else {
            insertNonFull(*root, k);
        }
    }
}

int main() {
    BTreeNode *root = NULL;
    int t = 3;
    int keys[] = {10, 20, 5, 6, 12, 30, 7, 17};
    for (int i = 0; i < sizeof(keys) / sizeof(keys[0]); i++) {
        insert(&root, keys[i], t);
    }

    printf("Traversal of the constructed B-tree is:");
    traverse(root);
    printf("\n");

    int k = 6;
    (search(root, k) != NULL) ? printf("Present\n") : printf("Not Present\n");

    k = 15;
    (search(root, k) != NULL) ? printf("Present\n") : printf("Not Present\n");

    return 0;
}