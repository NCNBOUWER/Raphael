#!/usr/bin/env python3
"""Metric-independent incidence + conventional comparison metrics.

These are *example* metrics, not inferred Raphael spacetime. No metric is
promoted to accepted Raphael theory. No physical laws inferred from scales.
"""
import json,math,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
PHI=(1+math.sqrt(5))/2

def euclidean_distance(a,b): return math.dist(a,b)

def logarithmic_radial_geodesic_distance(r1,r2,L=1):
    if r1<=0 or r2<=0 or L<=0:raise ValueError('positive r and L required')
    return L*abs(math.log(r2/r1))

def poincare_ball_distance(a,b,L=1):
    aa=sum(float(x)**2 for x in a);bb=sum(float(y)**2 for y in b)
    if aa>=1 or bb>=1 or L<=0:raise ValueError('unit ball only; L>0')
    dd=sum((float(x)-float(y))**2 for x,y in zip(a,b))
    return L*math.acosh(1+2*dd/((1-aa)*(1-bb)))

def spherical_circle_ratio(r,L):
    if L<=0 or r<=0:raise ValueError('positive r and L required')
    return math.pi*math.sin(r/L)/(r/L)

def tests():
    a,b,c=(0.0,0.0,0.0),(.2,0,0),(.1,.15,0)
    dAB=poincare_ball_distance(a,b);dBC=poincare_ball_distance(b,c);dAC=poincare_ball_distance(a,c)
    u=logarithmic_radial_geodesic_distance(1,PHI,2.3)
    v=logarithmic_radial_geodesic_distance(PHI,PHI**2,2.3)
    w=logarithmic_radial_geodesic_distance(1,2,2.3)
    sphere=spherical_circle_ratio(math.pi/2,1)
    assert abs(u-v)<1e-11
    assert abs(u-2.3*math.log(PHI))<1e-11
    assert abs(sphere-2)<1e-12
    assert dAB+dBC>=dAC-1e-12 and dAC>0
    assert abs(poincare_ball_distance(a,b)-poincare_ball_distance(b,a))<1e-13
    # Not a phi-only property. Arbitrary factor also has fixed log-scale steps.
    assert abs(w-2.3*math.log(2))<1e-11
    return {'logarithmic_metric':{'phi_step_at_L_2_3':u,'next_phi_step':v,'arbitrary_scale_2_step':w,'phi_is_not_unique':True},'spherical_geodesic_circle':{'ratio_at_r_pi_over_2':sphere,'pi_as_constant_irrational':True},'poincare_hyperbolic':{'triangle_inequality':True,'d_ab':dAB,'d_bc':dBC,'d_ac':dAC},'research_metric_conclusion':'illustrative only; Raphael metric unresolved'}
if __name__=='__main__':
    r=tests()
    (ROOT/'metric_test_results.json').write_text(json.dumps(r,indent=2))
    print(json.dumps(r,indent=2))
