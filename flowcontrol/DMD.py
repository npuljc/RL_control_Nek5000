"""
Author: Dr. Jichao Li <cfdljc@gmail.com>
Date:   2019-12-03
"""
import os
import numpy as np
import math
import scipy.stats as stats
import cmath
try:
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
except:
    pass

def xy(phi):
  return 1.0*np.cos(phi), 1.0*np.sin(phi)


class DMD_analysis(object):
    
    def __init__(self,dt,nr,A,B):
        '''
        dt: duration between snapshots
        nr: Number of POD modes
        A : Matrix A for snapshots
        B : Matrix B for snapshots
        '''    
        
        self.dt = dt
        self.nr = nr
        self.setmatrix(A,B)
        self.eigenW = None
        
    def setmatrix(self,A,B):
        '''
        Set matrix
        '''
        self.A = A
        self.B = B
        assert self.A.shape == self.B.shape
        self.nsnap = self.A.shape[1]
            
    def compute(self):
        '''
        Compute the DMD modes and eigenvalues
        '''
        tU, tomega, tV = np.linalg.svd(self.A, full_matrices=False)
        myU = tU[:,:self.nr]
        myV = np.transpose(tV[:self.nr,:])

        tmatrix = np.zeros((self.nr,self.nr))
        for i in range(self.nr):
            tmatrix[i,i] = 1.0/tomega[i]

        tempmatrix = np.dot(self.B, np.dot(myV[:,:], tmatrix))
        H = np.dot(np.transpose(myU), tempmatrix)

        eigenW, eigenV  = np.linalg.eig(H)
        
        self.eigenW = eigenW
    
    def growthrate(self):
        '''
        Select the __right__ eigenvalue to approximate the system's growth rate.
        We hacked it here:
        1. If the rate is too small (<<-10), pass
        2. If the frequency is too large, pass
        3. The right frequency for the confined cylinder case should be around 0.25-0.45
        '''
        growthrates=[]
        neigen = self.eigenW.shape[0]
        for i in range(neigen):
            thisspec  = cmath.log(self.eigenW[i])
            thisrate, thisfreqy = thisspec.real/self.dt, abs(thisspec.imag/(2.0*math.pi*self.dt))
            if thisfreqy > 0.45 or thisfreqy < 0.25: 
                growthrates.append(0.0)
            else:
                growthrates.append(thisrate)
        try:
            myindex = np.argmax(np.array(growthrates))
            return growthrates[myindex]
        except:
            return 0.0

    def ploteigen(self,filename):
        '''
        Plot the eigenvalues
        '''
        neigen = self.eigenW.shape[0]
        data = np.zeros((neigen,2))
        data_spetum = np.zeros((neigen,2))
        for i in range(neigen):
            data[i,0],data[i,1] = self.eigenW[i].real, self.eigenW[i].imag
            thisspec  = cmath.log(self.eigenW[i])
            data_spetum[i,0], data_spetum[i,1] = thisspec.real/self.dt, thisspec.imag/(2.0*math.pi*self.dt)
        
        phis=np.arange(0,6.28,0.01)
        circlex,circley = xy(phis)

        fontsize = 15
        fig = plt.figure(figsize=(10,5))
        gs = gridspec.GridSpec(1,2)
        gs.update(wspace=0.1, hspace=0.1)
        colorlabel = '#000000'
        colorinterval = '#2980b9'
        colorcl = colorinterval 
        colorcd = '#7f8c8d'
        colorback='#eaeaf2'#'#'
        iplot = 0
        ax = fig.add_subplot(gs[0,0])
        ax.set_xlim(-1.05,1.05)
        ax.set_ylim(-1.05,1.05)
        ax.set_axis_off
        ax.tick_params(
                        axis='both',          # changes apply to the x-axis
                        which='both',      # both major and minor ticks are affected
                        left=True,      # ticks along the bottom edge are off
                        labelleft=True,
                        labelright=False,
                        labelbottom=True,
                        right=False,         # ticks along the top edge are off
                        bottom=True,
                        top=False,
                        colors=colorlabel,
                        labelsize=fontsize,
                        width=0.2
                        )
        for myspline in ['top','left','right','bottom']:
            ax.spines[myspline].set_visible(True)
            ax.spines[myspline].set_color(colorlabel)
            ax.spines[myspline].set_linewidth(0.3)

        ax.plot(circlex,circley,color='#7f8c8d',lw=1.0,zorder=1)
        ax.scatter(data[:,0],data[:,1],color=colorcl,zorder=2)

        ax.set_xlabel(r'Re($\lambda$)',fontsize=fontsize,color=colorlabel)
        ax.set_ylabel(r'Im($\lambda$)',fontsize=fontsize,color=colorlabel)

        ax = fig.add_subplot(gs[0,1])
        ax.set_xlim(-1.0,5.0)
        ax.set_ylim(-2,2)
        ax.set_axis_off
        ax.tick_params(
                        axis='both',          # changes apply to the x-axis
                        which='both',      # both major and minor ticks are affected
                        left=True,      # ticks along the bottom edge are off
                        labelleft=True,
                        labelright=False,
                        labelbottom=True,
                        right=False,         # ticks along the top edge are off
                        bottom=True,
                        top=False,
                        colors=colorlabel,
                        labelsize=fontsize,
                        width=0.2
                        )
        for myspline in ['top','left','right','bottom']:
            ax.spines[myspline].set_visible(True)
            ax.spines[myspline].set_color(colorlabel)
            ax.spines[myspline].set_linewidth(0.3)

        ax.scatter(data_spetum[:,0],data_spetum[:,1],color=colorcl,zorder=2)

        ax.set_xlabel('Growth rate',fontsize=fontsize,color=colorlabel)
        ax.set_ylabel('Frequency',fontsize=fontsize,color=colorlabel)
               
        fig.savefig(filename+'.pdf',dpi=500, bbox_inches="tight")
        
