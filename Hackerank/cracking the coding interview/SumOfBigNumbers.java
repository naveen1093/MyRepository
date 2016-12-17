import java.io.*;
import java.util.*;
import java.math.*;
public class SumOfBigNumbers {

    public static void main(String[] args) {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Solution. */
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        BigInteger A = BigInteger.ZERO;     //long A=0L;
        while(n-- > 0){       
            A = A.add(BigInteger.valueOf(sc.nextInt()));     //A = A+sc.nextLong();
        }
        sc.close();
        System.out.println(A.toString());       //System.out.println(A);
    }
}
