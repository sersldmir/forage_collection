package twoMaxHeap;

import java.util.ArrayList;

public class NewHeap<T extends Comparable<T>>{

    private int childrenNumber;
    private ArrayList<T> heap;

    NewHeap(int x){
        this.childrenNumber = (int) Math.pow(2, x);
        this.heap = new ArrayList<>();
    }

    public void swap(int index1, int index2){
        T temp = this.heap.get(index1);
        this.heap.set(index1, this.heap.get(index2));
        this.heap.set(index2, temp);
    }

    public void heapifyUp(int index){
        while (true){
            int parentIndex = (int) Math.floor((index - 1)/this.childrenNumber);
            if (parentIndex == 0){
                break;
            } 
            else if (this.heap.get(index).compareTo(this.heap.get(parentIndex)) <= 0){
                break;
            }
            else{
                swap(index, parentIndex);
                index = parentIndex;
            }
        }
    }

    public int findMaxChild(int index){
        int res = (this.childrenNumber * index) + 1;
        for (int i = 2; i < this.childrenNumber; i++){
            int childIndex = (this.childrenNumber * index) + i;
            if (this.heap.get(res).compareTo(this.heap.get(childIndex)) <= 0){
                res = childIndex;
            }
        }
        return res;
    }

    public void heapifyDown(int index){
        while (true){
            if (index == this.heap.size() - 1){
                break;
            }
            else{
                int maxChildIndex = findMaxChild(index);
                if (this.heap.get(index).compareTo(this.heap.get(maxChildIndex)) >= 0){
                    break;
                }
                else{
                    swap(index, maxChildIndex);
                    index = maxChildIndex;
                }
            }
        }
    }

    public void insert(T element){
        this.heap.add(element);
        heapifyUp(this.heap.size() - 1);
    }

    public T popMax(){
        swap(0, this.heap.size() - 1);
        T maxElement = this.heap.remove(this.heap.size() - 1);
        heapifyDown(0);
        return maxElement;
    }
}