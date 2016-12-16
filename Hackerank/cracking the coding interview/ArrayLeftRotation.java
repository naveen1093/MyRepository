import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class ArrayLeftRotation {

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n = in.nextInt();
        int k = in.nextInt();
        int a[] = new int[n];
        for(int a_i=0; a_i < n; a_i++){
            a[a_i] = in.nextInt();
        }
        int rem = k%n; // rotating n times makes the array same as privous, optimize reminder is used
        int temp;
        int b[] = new int[n];
        for(int i=0;i<rem;i++){
            temp = a[0];
            int a_i;
            for(a_i=0; a_i < n-1; a_i++){
                a[a_i]=a[a_i+1];
            }
            a[n-1]=temp; // a[a_i] = temp;
        }
        for(int a_i=0; a_i < n; a_i++){
            System.out.print(a[a_i]+" ");
        }
        }
    }

Sample input:
5 4
1 2 3 4 5
Sample output:
5 1 2 3 4
