import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Created by s130973 on 17-3-2017.
 */
public class Algorithm1 {
    List<Pair> cpt = new ArrayList<>();

    public List sampleIndex(List<Tuple> S, Index I, int n) {
        for (Tuple t : S) {
            int count = lookup(t);

            Pair p = new Pair(t, count);
            cpt.add(p);
        }

        int sum = 0;
        for (Pair p : cpt){
            sum += p.getCount();
        }
        System.out.println(sum);

        List<Tuple> Sout = new ArrayList();

        List<Integer> sid = sampleRandomIntegers(n, sum);
        for (int id : sid) {
            int chosen = chosenTupleId(id, n);
            Tuple tS = cpt.get(chosen).getTuple();
            int offset = id - offsetId(chosen);
            Tuple tA = I.lookup(tS);
            Sout.add(tA);
            Sout.add(tS);
        }
        return Sout
    }

    public int lookup(Tuple t) {
        return 99;
    }

    //this method gives unique random integers with size Min(n, sum)
    private List<Integer> sampleRandomIntegers(int n, int sum) {
        int min = Math.min(sum, n);
        List<Integer> shuffleList = new ArrayList<>();
        for (int i = 0; i < sum; i++) {
            shuffleList.add(i,i);
        }
        Collections.shuffle(shuffleList);
        return shuffleList.subList(0, min);
    }

    private int chosenTupleId(int id, int n) {
        int sum = 0;
        for (int i = 0; i < n; i++) {
            sum += cpt.get(i).getCount();
            if (sum > id) {
                return i;
            }
        }
        System.out.println("Error in chosenTupleId");
        return -1;
    }
    private int offsetId(int chosen) {
        int sum = 0;
        if (chosen == 0) {
            return 0;
        }
        for (int i = 0; i < chosen; i++) {
            sum += cpt.get(i).getCount()
        }
        return sum;
    }
}
