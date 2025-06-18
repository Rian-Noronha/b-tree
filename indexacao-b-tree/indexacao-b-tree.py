# Define a estrutura de um nó da B-Tree.
class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf  # Flag: True se o nó é uma folha (não tem filhos).
        self.keys = []    # Lista de chaves (valores) ordenada no nó.
        self.child = []   # Lista de ponteiros para os nós filhos.

# Define a estrutura da B-Tree e suas operações principais.
class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)  # A raiz da árvore, que começa como uma folha.
        self.t = t                   # Grau mínimo (ordem 't'). Define a capacidade dos nós.

    # Busca uma chave 'k' na sub-árvore a partir de 'node'.
    def search(self, k, node=None):
        if node is None:
            node = self.root
        
        # Encontra a posição da chave ou o filho a ser seguido.
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        
        # Chave encontrada neste nó.
        if i < len(node.keys) and k == node.keys[i]:
            return (node, i)
        
        # Se o nó é folha, a busca falha.
        if node.leaf:
            return None
        
        # Desce recursivamente para o filho apropriado.
        return self.search(k, node.child[i])

    # Método público para inserir uma chave 'k'.
    def insert(self, k):
        root = self.root
        # Se a raiz está cheia, a árvore cresce em altura.
        if len(root.keys) == (2 * self.t) - 1:
            # Cria uma nova raiz, e a antiga vira sua filha.
            new_root = BTreeNode()
            self.root = new_root
            new_root.child.insert(0, root)
            # Divide a antiga raiz (agora filha).
            self._split_child(new_root, 0)
            # Insere a chave na nova estrutura.
            self._insert_non_full(new_root, k)
        else:
            # Se há espaço, insere na sub-árvore da raiz.
            self._insert_non_full(root, k)

    # Insere uma chave 'k' em um nó 'node' que garantidamente não está cheio.
    def _insert_non_full(self, node, k):
        i = len(node.keys) - 1
        # Caso base: se o nó é uma folha, insere a chave na posição correta.
        if node.leaf:
            node.keys.append(0) # Expande a lista para abrir espaço.
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
        # Caso recursivo: se o nó é interno.
        else:
            # Encontra o filho que deve receber a nova chave.
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            # Antes de descer, verifica se o filho está cheio.
            if len(node.child[i].keys) == (2 * self.t) - 1:
                # Se estiver, divide o filho para abrir espaço.
                self._split_child(node, i)
                # Após a divisão, decide em qual dos novos filhos a chave se encaixa.
                if k > node.keys[i]:
                    i += 1
            # Desce recursivamente para inserir no filho apropriado.
            self._insert_non_full(node.child[i], k)

    # Divide o filho 'i' (que está cheio) do nó 'parent'.
    def _split_child(self, parent, i):
        t = self.t
        full_child = parent.child[i]
        new_child = BTreeNode(full_child.leaf) # O novo nó tem a mesma natureza (folha ou não).

        # A chave mediana do filho sobe para o nó pai.
        parent.keys.insert(i, full_child.keys[t - 1])
        parent.child.insert(i + 1, new_child)

        # As chaves maiores do filho cheio são movidas para o novo nó.
        new_child.keys = full_child.keys[t:(2 * t) - 1]
        # As chaves menores permanecem no filho original.
        full_child.keys = full_child.keys[0:(t - 1)]

        # Se o nó não era folha, distribui também os filhos.
        if not full_child.leaf:
            new_child.child = full_child.child[t:(2 * t)]
            full_child.child = full_child.child[0:t]

    # Método público para remover uma chave 'k'.
    def delete(self, k):
        self._delete_internal(self.root, k)
        # Se a raiz ficou sem chaves, a árvore encolhe em altura.
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.child[0]

    # Lógica recursiva principal para remoção a partir de 'node'.
    def _delete_internal(self, node, k):
        t = self.t
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        # Caso 1: A chave 'k' está no nó atual.
        if i < len(node.keys) and node.keys[i] == k:
            if node.leaf: # Subcaso 1.1: Se é folha, apenas remove.
                node.keys.pop(i)
            else: # Subcaso 1.2: Se é nó interno, a lógica é mais complexa.
                # Se o filho esquerdo tem chaves suficientes, substitui 'k' pelo seu predecessor.
                if len(node.child[i].keys) >= t:
                    pred = self._get_predecessor(node, i)
                    node.keys[i] = pred
                    self._delete_internal(node.child[i], pred)
                # Senão, se o filho direito tem chaves suficientes, usa o sucessor.
                elif len(node.child[i + 1].keys) >= t:
                    succ = self._get_successor(node, i)
                    node.keys[i] = succ
                    self._delete_internal(node.child[i + 1], succ)
                # Se ambos os filhos têm poucas chaves, faz o merge deles.
                else:
                    self._merge(node, i)
                    self._delete_internal(node.child[i], k)
        # Caso 2: A chave 'k' não está no nó atual, desce para um filho.
        elif not node.leaf:
            # Garante que o filho para onde vamos descer tem chaves suficientes.
            if len(node.child[i].keys) < t:
                self._fix_child(node, i) # Se não tiver, corrige antes de descer.
            self._delete_internal(node.child[i], k)

    # Encontra a maior chave na sub-árvore esquerda (predecessor).
    def _get_predecessor(self, node, i):
        curr = node.child[i]
        while not curr.leaf:
            curr = curr.child[-1] # Desce sempre para o filho mais à direita.
        return curr.keys[-1]

    # Encontra a menor chave na sub-árvore direita (sucessor).
    def _get_successor(self, node, i):
        curr = node.child[i + 1]
        while not curr.leaf:
            curr = curr.child[0] # Desce sempre para o filho mais à esquerda.
        return curr.keys[0]

    # Funde (merge) o filho 'i' com seu irmão 'i+1'.
    def _merge(self, node, i):
        child = node.child[i]
        sibling = node.child[i + 1]

        # A chave do pai desce para unir os dois filhos.
        child.keys.append(node.keys.pop(i))
        # As chaves e filhos do irmão são anexados.
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.child.extend(sibling.child)

        # Remove o ponteiro para o irmão, que agora está vazio.
        node.child.pop(i + 1)

    # Corrige um filho 'i' que tem poucas chaves (< t), usando seus irmãos.
    def _fix_child(self, node, i):
        t = self.t
        # Tenta emprestar uma chave do irmão esquerdo.
        if i != 0 and len(node.child[i - 1].keys) >= t:
            left = node.child[i - 1]
            curr = node.child[i]
            # Chave do pai desce para o nó atual, chave do irmão sobe para o pai.
            curr.keys.insert(0, node.keys[i - 1])
            if not left.leaf:
                curr.child.insert(0, left.child.pop())
            node.keys[i - 1] = left.keys.pop()
        # Senão, tenta emprestar do irmão direito.
        elif i != len(node.child) - 1 and len(node.child[i + 1].keys) >= t:
            right = node.child[i + 1]
            curr = node.child[i]
            # Mesma lógica de rotação de chaves.
            curr.keys.append(node.keys[i])
            if not right.leaf:
                curr.child.append(right.child.pop(0))
            node.keys[i] = right.keys.pop(0)
        # Se não for possível emprestar, faz o merge.
        else:
            if i != len(node.child) - 1:
                self._merge(node, i)
            else:
                self._merge(node, i - 1)

    # Imprime a árvore de forma hierárquica para visualização.
    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        print("  " * level + str(node.keys)) # Indentação representa a profundidade.
        if not node.leaf:
            for child in node.child:
                self.print_tree(child, level + 1)

# Bloco principal para instanciar e demonstrar o uso da B-Tree.
if __name__ == "__main__":
    print("Simulador de Índice de Registros Genômicos com B-Tree\n")
    # Instancia a árvore com grau mínimo 3.
    genome_index = BTree(3)

    # Insere uma lista de chaves.
    record_ids = [10, 20, 5, 6, 12, 30, 7, 17, 50, 60, 25, 35, 45, 55, 65, 75]
    for record_id in record_ids:
        genome_index.insert(record_id)

    print("\nEstrutura da árvore após inserções:")
    genome_index.print_tree()

    # Remove uma lista de chaves.
    delete_ids = [6, 17, 10]
    for del_id in delete_ids:
        print(f"\nRemovendo {del_id}:")
        genome_index.delete(del_id)
        genome_index.print_tree()