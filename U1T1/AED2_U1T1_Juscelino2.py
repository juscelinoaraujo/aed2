# -*- coding: utf-8 -*-

import requests
response = requests.get("https://raw.githubusercontent.com/juscelinoaraujo/aed2/main/U1T1/biblia-em-txt.txt")

print(response.text)
biblia_string = response.text

caracteres_removiveis = "0123456789,.;?[]{}'!@#$%&*()_^:"
for c in caracteres_removiveis:
  biblia_string = biblia_string.replace(c, "")


biblia_string = biblia_string.lower()

biblia_string = biblia_string.replace("\n", " ")
biblia_string = biblia_string.replace("\r", " ")
biblia_string = biblia_string.replace("-", " ")
biblia_lista = biblia_string.split(" ")

biblia_lista = list(set(biblia_lista))

palavras_removiveis = [" ", "o", "os", "a", "as", "um", "uma", "de", "do", "dos", "da", "das", "dum", "duma", "em", "no", "nos", "na", "nas", "para", "que", "mas", "e", "se"]
for p in palavras_removiveis:
  if p in biblia_lista:
    biblia_lista.remove(p)

biblia_lista = list(set(biblia_lista))
biblia_lista_ordenada = sorted(biblia_lista)


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

def autocomplete_lista_ordenada(lista, palavra):
  saida = []
  for p in lista:
    if p[0:len(palavra)] < palavra:
      continue
    elif p[0:len(palavra)] == palavra:
      saida.append(p)
    else:
      break;
  return saida

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

def autocomplete_arvore_AVL(arvore, prefixo):
  return sorted(autocomplete_no(arvore.root, prefixo))

biblia_arvore_AVL = AVLTree();
for p in biblia_lista_ordenada:
  biblia_arvore_AVL.add(p)

prefixos_teste = ["aba", "abs", "bala", "cer", "dar", "ef", "gala", "jav", "jo", "lamu", "ob", "ol", "pra", "quer", "ru", "sal", "tab", "val", "xen", "zel"]

import time
resultados_lista = []
resultados_arvore = []
for p in prefixos_teste:
  t_inicial = time.time_ns()
  autocomplete_lista_ordenada(biblia_lista_ordenada, p)
  t_final = time.time_ns()
  resultados_lista.append(t_final - t_inicial)
  t_inicial = time.time_ns()
  autocomplete_arvore_AVL(biblia_arvore_AVL, p)
  t_final = time.time_ns()
  resultados_arvore.append(t_final - t_inicial)

import matplotlib.pyplot as plt
import numpy as np
resultados_proporcao = [arvore/lista for arvore, lista in zip(resultados_arvore, resultados_lista)]

x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
plt.plot(x, resultados_proporcao)
plt.xlabel("Prefixos de teste")
plt.ylabel("Razão do tempo árvore/lista")
plt.title("Razão do tempo necessário de autocompletamento por busca em árvore para busca em lista")
plt.show()

!pip install streamlit
import streamlit as st
st.header("Autocompletamento de Palavras da Bíblia")
st.write("A ferramenta a seguir busca palavras na Bíblia que comecem com o prefixo preenchido no campo abaixo.")

prefixo = st.text_input("Digite o prefixo que deseja pesquisar: ")

if len(prefixo) != 0:
  st.write(autocomplete_arvore_AVL(biblia_arvore_AVL, prefixo))
