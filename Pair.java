/**
 * Created by s130973 on 17-3-2017.
 */
public class Pair
{
    private Tuple t;
    private int count;

    public Pair(Tuple t, int count)
    {
        this.t = t;
        this.count = count;
    }

    public Tuple getTuple() {
        return t;
    }

    public int getCount() {
        return count;
    }
}