import java.io.*;

public class StatisticalAnalysis implements IStatisticalAnalysis{

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int[] array= {2,2,2,2,2,5};
		System.out.println(new StatisticalAnalysis().getMeanCrossingRate(array));
		
	}

	@Override
	public float getMean(int[] array) {
	     int sum = 0;
	      for(int i = 0; i < array.length; i++) {
	         sum+=array[i];
	      }
		return sum/(float) (array.length);
	}

	@Override
	public float getVariance(int[] array) {
		// TODO Auto-generated method stub
		// The mean average
		double mean = 0.0;
		for (int i = 0; i < array.length; i++) {
		        mean += array[i];
		}
		mean /= array.length;
		// The variance
		double variance = 0;
		for (int i = 0; i < array.length; i++) {
		    variance += Math.pow((array[i] - mean),2) ;
		}
		variance /= array.length;
		return (float) variance;
	} 

	@Override
	public float getEnergy(int[] array) {
		// TODO Auto-generated method stub
		double energy=0.0;
		for(int i=0; i<array.length;i++) {
			energy+=Math.pow(array[i],2);
		}
		return (float) (energy/(array.length));
	}

	@Override
	public float getAvgAbs(int[] array) {
		// TODO Auto-generated method stub
		double mean = 0.0;
		for (int i = 0; i < array.length; i++) {
		        mean += array[i];
		}
		mean /= array.length;
        float absSum = 0; 
        int n = array.length;
        for (int i = 0; i < n; i++) 
            absSum = (float) (absSum + Math.abs(array[i] 
                                - mean)); 
      
        return absSum / n; 
	}

	@Override
	public float getSkew(int[] array) {
		// TODO Auto-generated method stub
		   int n = array.length;
		   
		   int sum = 0;
		      for(int i = 0; i < n; i++) {
		         sum+=array[i];
		      }
		   double mean = sum/(float) (array.length);

		   double x = 0,y=0;
		   for(int i = 0 ; i <n;i++)
		   {
			  x+= Math.pow((array[i]-mean),3);
		   }
		   	  x/=n;

		   for(int i = 0 ; i < n ;i++) {
			  y+= Math.pow((array[i]-mean),2);
		   }

		   y/=n;
		   y=Math.pow(Math.sqrt(y),3);

		   
		   return (float) (x/y);
		   
	}

	@Override
	public float getKurt(int[] array) {
		// TODO Auto-generated method stub

		   int n = array.length;
		   
		   int sum = 0;
		      for(int i = 0; i < n; i++) {
		         sum+=array[i];
		      }
		   double mean = sum/(float) (array.length);
		   
		   double x=0,y=0;
		   	  for(int i=0; i<n;i++) {
		   		  x+=Math.pow((array[i]-mean),4);
		   	  }
		   	  x/=n;
		   	  for(int i=0; i<n;i++) {
		   		  y+=Math.pow((array[i]-mean),2);
		   	  }
		   	  y/=n;
		   	  y=Math.pow(y,2);
		return (float) (x/y);
	}

	@Override
	public float getRootMeanSquare(int[] array) {
		// TODO Auto-generated method stub
		int n= array.length;
		int square = 0; 
	    float mean = 0; 
	    float root = 0; 
	  
	    // Calculate square. 
	    for(int i = 0; i < n; i++) 
	    { 
	        square += Math.pow(array[i], 2); 
	    } 
	      
	    // Calculate Mean.  
	    mean = (square / (float) (n)); 
	  
	    // Calculate Root. 
	    root = (float)Math.sqrt(mean); 
	  
	    return root; 
	}

	@Override
	public float getZeroCrossingRate(int[] array) {
		// TODO Auto-generated method stub
		int ans=0;
		for(int i=1;i<array.length;i++) {
			ans+=Math.abs(isPositive((array[i]))-isPositive((array[i-1])));
		}
		
		return ans;
	}

	@Override
	public float getMeanCrossingRate(int[] array) {
		// TODO Auto-generated method stub
		int n = array.length;
		int sum = 0;
		for(int i = 0; i < n; i++) {
		         sum+=array[i];
		      }
		double mean = sum/(float) (array.length);
		int ans=0;
		for(int i=1;i<array.length;i++) {
			ans+=Math.abs(isPositive((array[i])-mean)-isPositive((array[i-1])-mean));
		}
		
		
		return ans;
	}
	int isPositive(double num) {
		if(num<0) 
			return 0;
		else
			return 1;
		
	}
	
}
