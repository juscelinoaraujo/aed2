# -*- coding: utf-8 -*-

import requests
response = requests.get("https://raw.githubusercontent.com/juscelinoaraujo/aed2/main/U1T1/biblia-em-txt.txt")

print(response.text)
biblia_string = response.text

# Em seguida, são removidos caracteres especiais, incluindo números e sinais de pontuação."""

caracteres_removiveis = "0123456789,.;?[]{}'!@#$%&*()_^:"
for c in caracteres_removiveis:
  biblia_string = biblia_string.replace(c, "")

# O passo seguinte é a conversão de todas as letras para minúsculas."""

biblia_string = biblia_string.lower()

# Além disso, letras (no caso do português somente as vogais) com acentuação tem seus acentos removidos."""

#a_com_acento = "áàãâ"
#e_com_acento = "éê"
#o_com_acento = "óõô"
#for l in a_com_acento:
#  biblia_string = biblia_string.replace(l, "a")
#for l in e_com_acento:
#  biblia_string = biblia_string.replace(l, "e")
#for l in o_com_acento:
#  biblia_string = biblia_string.replace(l, "o")
#biblia_string = biblia_string.replace("í", "i")
#biblia_string = biblia_string.replace("ú", "u")
#biblia_string = biblia_string.replace("ç", "c")

# Removidos os caracteres especiais e trocadas as letras com acentos, a string é dividida em palavras. A separação acontece por meio de espaços. Por isso, as quebras de linhas e os hífens são inicialmente convertidas em espaços para que a separação ocorra normalmente. Com isso, é criado o arquivo `biblia_lista`, que consiste em uma lista com as palavras obtidas da separação realizada."""

biblia_string = biblia_string.replace("\n", " ")
biblia_string = biblia_string.replace("-", " ")
biblia_lista = biblia_string.split(" ")

# Algumas das palavras não são de interesse, como artigos, preposições e algumas conjunções. Elas são retiradas da lista."""

palavras_removiveis = [" ", "o", "os", "a", "as", "um", "uma", "de", "do", "dos", "da", "das", "dum", "duma", "em", "no", "nos", "na", "nas", "para", "que", "mas", "e", "se"]
for p in palavras_removiveis:
  if p in biblia_lista:
    biblia_lista.remove(p)

# Como seria de se esperar um texto tão grande, muitas palavras são repetidas. O código executado a seguir remove as palavras repetidas. Isso é feito gerando uma estrutura de conjunto com os elementos da lista e depois gerando uma nova lista a partir desse conjunto. Convém lembrar que isso advém do fato de que em estruturas de tipo conjunto não há multiplicidade de elementos."""

biblia_lista = list(set(biblia_lista))

# A lista de palavras é então ordenada, sendo armazenada na variável `biblia_lista_ordenada`:"""

biblia_lista_ordenada = sorted(biblia_lista)

# Já temos uma lista de palavras, o que funcionará como estrutura linear de busca para efeitos de comparção. Quanto à estrutura em árvore, na seção a seguir são descritas as classes previamente criadas e que seriam utilizadas aqui.

### Árvores AVL

class Node:

    def __init__(self, value):
        
        self.value = value
        self.left_child = None
        self.right_child = None

class BST:

    def __init__(self):
        
        self.root = None

    def add(self, value):
        
        if self.root is None:
            self.root = Node(value)
        else:
            self._add_recursive(self.root, value)

    def _add_recursive(self, current_node, value):
        
        if value <= current_node.value:
            if current_node.left_child is None:
                current_node.left_child = Node(value)
            else:
                self._add_recursive(current_node.left_child, value)
        else:
            if current_node.right_child is None:
                current_node.right_child = Node(value)
            else:
                self._add_recursive(current_node.right_child, value)

    def _contains(self, current_node, value):
       
        if current_node is None:
            return False
        if current_node.value == value:
            return True
        if value < current_node.value:
            return self._contains(current_node.left_child, value)
        return self._contains(current_node.right_child, value)

    def contains(self, value):
        return self._contains(self.root, value)
        
class AVLNode(Node):

    def __init__(self, value):
        
        super().__init__(value)
        self.height = 1
        self.imbalance = 0

    def calculate_height_and_imbalance(self):
        
        # Calculate the height of the left child subtree
        left_height = 0
        if self.left_child is not None:
            left_height = self.left_child.height

        # Calculate the height of the right child subtree
        right_height = 0
        if self.right_child is not None:
            right_height = self.right_child.height

        # Update the height of this node
        self.height = 1 + max(left_height, right_height)

        # Calculate and update the imbalance factor for this node
        self.imbalance = left_height - right_height

class AVLTree(BST):

    def __init__(self):
        
        super().__init__()

    def add(self, value):
        
        self.root = self._add_recursive(self.root, value)  # Note that self.root is updated here


    def _add_recursive(self, current_node, value):

        # If the current node is None, return a new AVLNode containing the value
        if current_node is None:
            return AVLNode(value)

        # Check if current_node is of the base class Node and cast it to AVLNode if necessary
        # This is necessary to not change the add() in the BST class.
        # When the first node is added, the type of the root is Node, so we need to cast it
        if isinstance(current_node, Node) and not isinstance(current_node, AVLNode):
            current_node = AVLNode(current_node.value)
            current_node.left_child = self.root.left_child
            current_node.right_child = self.root.right_child
            self.root = current_node

        # Determine whether the value should be inserted to the left or right subtree
        if value <= current_node.value:
            current_node.left_child = self._add_recursive(current_node.left_child, value)
        else:
            current_node.right_child = self._add_recursive(current_node.right_child, value)

        # Update the height and imbalance factor for the current node
        current_node.calculate_height_and_imbalance()

        # Check if tree balancing is needed and balance if necessary
        if abs(current_node.imbalance) == 2:
            return self._balance(current_node)

        return current_node

    def get_height(self):
        
        if self.root is None:
            return 0
        return self.root.height

    def _rotate_left(self, node):
        

        # Store the pivot (the root of the right subtree of 'node')
        pivot = node.right_child

        # Update the right child of 'node' to be the left child of the pivot
        node.right_child = pivot.left_child

        # Set the left child of the pivot to be the node
        pivot.left_child = node

        # Recalculate the height and imbalance factor for the rotated node
        node.calculate_height_and_imbalance()

        # Recalculate the height and imbalance factor for the pivot
        pivot.calculate_height_and_imbalance()

        # Return the pivot as the new root of this subtree
        return pivot


    def _rotate_right(self, node):
        

        # Store the pivot (the root of the left subtree of 'node')
        pivot = node.left_child

        # Update the left child of 'node' to be the right child of the pivot
        node.left_child = pivot.right_child

        # Set the right child of the pivot to be the node
        pivot.right_child = node

        # Recalculate the height and imbalance factor for the rotated node
        node.calculate_height_and_imbalance()

        # Recalculate the height and imbalance factor for the pivot
        pivot.calculate_height_and_imbalance()

        # Return the pivot as the new root of this subtree
        return pivot

    def _balance(self, node):
      

      # Case 1: Left subtree is higher than right subtree
      if node.imbalance == 2:
          pivot = node.left_child
          # Single right rotation
          if pivot.imbalance == 1:
              return self._rotate_right(node)
          # Double rotation: Left-Right
          else:
              node.left_child = self._rotate_left(pivot)
              return self._rotate_right(node)
      # Case 2: Right subtree is higher than left subtree
      else:
          pivot = node.right_child
          # Single left rotation
          if pivot.imbalance == -1:
              return self._rotate_left(node)
          # Double rotation: Right-Left
          else:
              node.right_child = self._rotate_right(pivot)
              return self._rotate_left(node)


### Função de Autocompletamento de Palavras

def autocomplete_no(no, prefixo):
  saida = []
  if no != None:
    inicio = no.value[0:len(prefixo)]
    if inicio >= prefixo:
      saida += autocomplete_no(no.left_child, prefixo)
    if inicio == prefixo:
      saida.append(no.value)
    if inicio <= prefixo:
      saida += autocomplete_no(no.right_child, prefixo)
  return saida

def autocomplete_arvore_AVL(arvore, palavra):
  return sorted(autocomplete_no(arvore.root, palavra))

biblia_arvore_AVL = AVLTree();
for p in biblia_lista_ordenada:
  biblia_arvore_AVL.add(p)

import streamlit as st
prefixo = st.text_input("Digite o prefixo que deseja pesquisar: ")
lista_palavras = autocomplete_arvore_AVL(biblia_arvore_AVL, prefixo)
st.write(lista_palavras)
