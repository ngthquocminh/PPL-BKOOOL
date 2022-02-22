
public class A {
    public int GetI() {
        return this.i;
    }
    public int GetO() {
        return 5;
    }
    int i = GetI();
    public static void main(String[] args) {
        C c = new C();
        c.b = new B();
        String[]  arr = {"1","2","3","","","","","","","","","","","","","","","","",""};
        final int _i = 9;
        final String me = "me";
        String _x = "C";
        c.b.text = arr[_i];
        System.out.println(B.cname);
    }
}
