public class PairMultiplicationOf2Array {
	public static void main(String[] args)
	 {
	      int a[] = {3,4,5,6};
	      int b[] = {1,2};
	      int r = mul(a,b);
	      System.out.println(r);
	 }
	public static int mul(int[] a, int []b) {
	      int res=0, resrow, i, j;
	      for (i=0 ; i<a.length ; i++) {
	            for (resrow=j=0 ; j<b.length ; j++) {
	            	
	                 resrow = resrow * 10 + a[i] * b[j];
	                 System.out.println(resrow);
	            }
	            res = res * 10 + resrow;
	      }
	      return res;
	 }
}
