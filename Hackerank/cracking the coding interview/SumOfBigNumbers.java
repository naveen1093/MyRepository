import java.io.*;
import java.util.*;
import java.math.*;
public class SumOfBigNumbers {

    public static void main(String[] args) {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Solution. */
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        BigInteger A = BigInteger.ZERO;
        while(n-- > 0){
        String str = sc.next();
            A = A.add(new BigInteger(str));
        }
        sc.close();
        System.out.println(A.toString());
    }
}
