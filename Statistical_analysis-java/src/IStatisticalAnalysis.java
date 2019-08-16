
public interface IStatisticalAnalysis {
	
	public float getMean(int[] array);
	public float getVariance(int[] array);
	public float getEnergy(int[] array);
	public float getAvgAbs(int[] array);
	public float getSkew(int[] array);
	public float getKurt(int[] array);
	public float getRootMeanSquare(int[] array);
	public float getZeroCrossingRate(int[] array);
	public float getMeanCrossingRate(int[] array);
	
}
