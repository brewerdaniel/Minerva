/*
 * Automatic 3 axis calibration.
 * 
 * This method of calibration is an extension of the 2D method described at
 * http://www.fatquarterssoftware.com/downloads/AUTOCAL.pdf
 * 
 * While that paper says that extension to 3D is obvious, it doesn't mention
 * that is isn't simple. The math is really pretty simple but keeping track
 * of the details is tedious.
 * 
 * Using this method you do not have to carefully find the minimum and maximum
 * responses from the sensor. Just pick 6 reasonably distinct measurement
 * sets and go.
 * 
 * Oct. 2009 David W. Schultz
 */

#include <stdio.h>
#include <math.h>


/*
 * Matrix code snarfed from: http://www.hlevkin.com/NumAlg/LinearEquations.c
 */
//==============================================================================
//return 1 if system
	not solving
		// nDim - system dimension
		// pfMatr - matrix with coefficients
		// pfVect - vector with free members
		// pfSolution - vector with system solution
		// pfMatr becames trianglular after function call
		// pfVect changes after function call
		//
//Developer:	Henry Guennadi Levkin
		//
		//==============================================================================
		int		LinearEquationsSolving(int nDim, float *pfMatr, float *pfVect, float *pfSolution){
	float		fMaxElem;
	float		fAcc;

	int		i         , j, k, m;


	for (k = 0; k < (nDim - 1); k++)
		//base row of matrix
	{
		//search of line with max element
			fMaxElem = fabs(pfMatr[k * nDim + k]);
		m = k;
		for (i = k + 1; i < nDim; i++) {
			if (fMaxElem < fabs(pfMatr[i * nDim + k])) {
				fMaxElem = pfMatr[i * nDim + k];
				m = i;
			}
		}

		//permutation of base line(index k) and max element line(index m)
		if              (m != k) {
			for (i = k; i < nDim; i++) {
				fAcc = pfMatr[k * nDim + i];
				pfMatr[k * nDim + i] = pfMatr[m * nDim + i];
				pfMatr[m * nDim + i] = fAcc;
			}
					fAcc =	pfVect [k];
			pfVect[k] = pfVect[m];
			pfVect[m] = fAcc;
		}
		if (pfMatr[k * nDim + k] == 0.)
			return 1;
		//needs improvement ! !!

			//triangulation of matrix with coefficients
			for (j = (k + 1); j < nDim; j++)
			//current row of matrix
		{
			fAcc = -pfMatr[j * nDim + k] / pfMatr[k * nDim + k];
			for (i = k; i < nDim; i++) {
				pfMatr[j * nDim + i] = pfMatr[j * nDim + i] + fAcc * pfMatr[k * nDim + i];
			}
			pfVect[j] = pfVect[j] + fAcc * pfVect[k];
			//free member recalculation
		}
	}

	for (k = (nDim - 1); k >= 0; k--) {
		pfSolution[k] = pfVect[k];
		for (i = (k + 1); i < nDim; i++) {
			pfSolution[k] -= (pfMatr[k * nDim + i] * pfSolution[i]);
		}
		pfSolution[k] = pfSolution[k] / pfMatr[k * nDim + k];
	}

	return 0;
	}

	/*
	 * x, y, z are vectors of six measurements
	 * 
	 * Computes sensitivity and offset such that:
	 * 
	 * c = s * A + O
	 * 
	 * where c is the measurement, s is the sensitivity, O is the offset,
	 * and A is the field being measured  expressed as a ratio of the
	 * measured value to the field strength. aka a direction cosine.
	 * 
	 * A is what we really want and it is computed using the equation:
	 * 
	 * A = (c - O)/s
	 * 
	 */


	int		cal        (float *x, float *y, float *z, float *S, float *O){
		int		i;
		float		A        [25], *p;
		float		f        [5], X[5];
		float		k1      , k2;

		/* Fill in matrix A */

		p = A;
		for (i = 0; i < 5; i++) {
			*p++ = 2.0 * (x[i] - x[i + 1]);
			*p++ = y[i + 1] * y[i + 1] - y[i] * y[i];
			*p++ = 2.0 * (y[i] - y[i + 1]);
			*p++ = z[i + 1] * z[i + 1] - z[i] * z[i];
			*p++ = 2.0 * (z[i] - z[i + 1]);
			f[i] = x[i] * x[i] - x[i + 1] * x[i + 1];
		}
		/* Solve AX=f */

		if (LinearEquationsSolving(5, A, f, X)) {
			fprintf(stderr, "System not solvable\n");
			return -1;
		}
		/* Compute sensitivities and offsets */

		k1 = X[1];
		k2 = X[3];
		O[0] = X[0];
		O[1] = X[2] / k1;
		O[2] = X[4] / k2;

		S[0] = sqrt((x[5] - O[0]) * (x[5] - O[0]) +
			    k1 * (y[5] - O[1]) * (y[5] - O[1]) +
			    k2 * (z[5] - O[2]) * (z[5] - O[2]));
		S[1] = sqrt(S[0] * S[0] / k1);
		S[2] = sqrt(S[0] * S[0] / k2);
		return 0;
	}

	/*
	 * Test data captured from an ADXL335 accelerometer (series 1) and a
	 * HMC5843 magnetometer (series 2). I tried to orient the
	 * accelerometer to get +/-1G for each sensor and was more or less
	 * succesful. Picking good orientations for the magnetic sensor more
	 * difficult so I didn't try. It just got whatever fell out of what I
	 * picked based on the accel.
	 */
	float		X1       [] = {2021, 2424, 2008, 1606, 1950, 2032};
	float		Y1       [] = {2439, 2028, 1612, 2021, 2025, 1979};
	float		Z1       [] = {2064, 2059, 2038, 2046, 1622, 2437};

	float		X2       [] = {-30, -748, 112, 746, 548, -440};
	float		Y2       [] = {-783, 105, 815, 119, 93, 205};
	float		Z2       [] = {370, 432, 387, -421, 680, -651};

	/*
	 * Simple test of calibration code. Compute the calibration values
	 * for each series and then process each data point.
	 */
	int		main       () {
		int		i;
		float		Sens     [3], Offset[3];
		float		x       , y, z;

		if (cal(X1, Y1, Z1, Sens, Offset) == 0) {
			printf(" X       Y       Z\n");
			printf("Sens:   %10.5f %10.5f %10.5f\n", Sens[0], Sens[1], Sens[2]);
			printf("Offset: %10.5f %10.5f %10.5f\n", Offset[0], Offset[1], Offset[2]);

			for (i = 0; i < 6; i++) {
				x = (X1[i] - Offset[0]) / Sens[0];
				y = (Y1[i] - Offset[1]) / Sens[1];
				z = (Z1[i] - Offset[2]) / Sens[2];

				printf("%7.2f %7.2f %7.2f %10f\n",
				       acos(x) * 180 / M_PI,
				       acos(y) * 180 / M_PI,
				       acos(z) * 180 / M_PI, sqrt(x * x + y * y + z * z));
			}
		}
		if (cal(X2, Y2, Z2, Sens, Offset) == 0) {
			printf(" X       Y       Z\n");
			printf("Sens:   %10.5f %10.5f %10.5f\n", Sens[0], Sens[1], Sens[2]);
			printf("Offset: %10.5f %10.5f %10.5f\n", Offset[0], Offset[1], Offset[2]);

			for (i = 0; i < 6; i++) {
				x = (X2[i] - Offset[0]) / Sens[0];
				y = (Y2[i] - Offset[1]) / Sens[1];
				z = (Z2[i] - Offset[2]) / Sens[2];

				printf("%7.2f %7.2f %7.2f %10f\n",
				       acos(x) * 180 / M_PI,
				       acos(y) * 180 / M_PI,
				       acos(z) * 180 / M_PI, sqrt(x * x + y * y + z * z));
			}
		}
	}
