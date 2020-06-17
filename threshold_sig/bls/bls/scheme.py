"""
BLS signature scheme.
Example:
	>>> m = [3] * 2 # messages
	>>> t, n = 2, 3 # number of authorities
	>>> params = setup() # generate the public parameters.
	>>> (sk, vk) = ttp_keygen(params, t, n) # generate key
	>>> aggr_vk = aggregate_vk(params, vk) # aggregate verification keys
	>>> sigs = [sign(params, ski, m) for ski in sk] # sign
	>>> sigma = aggregate_sigma(params, sigs) # aggregate credentials
	>>> assert verify(params, aggr_vk, sigma, m) # verify signature
"""
from bplib.bp import BpGroup, G2Elem
from bls.utils import *


def setup():
	"""
	Generate the public parameters.

	Returns:
		- params: the publc parameters
	"""
	G = BpGroup()
	(g1, g2) = G.gen1(), G.gen2()
	(e, o) = G.pair, G.order()
	return (G, o, g1, g2, e)


def ttp_keygen(params, t, n):
	"""
	Generate keys for threshold signature (executed by a TTP).

	Parameters:
		- `params`: public parameters generated by `setup`
		- `t` (integer): the threshold parameter
		- `n` (integer): the total number of authorities

	Returns:
		- `sk` [Bn]: array containing the secret key of each authority
		- `vk` [G2Elem]: array containing the verification key of each authority
	"""
	assert n >= t and t > 0
	(G, o, g1, g2, e) = params
	# generate polynomials
	v = [o.random() for _ in range(0,t)]
	# generate shares
	sk = [poly_eval(v,i) % o for i in range(1,n+1)]
	# set keys
	vk = [xi*g2 for xi in sk]
	return (sk, vk)


def aggregate_vk(params, vks, threshold=True):
	"""
	Aggregate the verification keys.

	Parameters:
		- `params`: public parameters generated by `setup`
		- `vks` [G2Elem]: array containing the verification key of each authority
		- `threshold` (bool): optional, whether to use threshold cryptography or not

	Returns:
		- `aggr_vk` (G2Elem): aggregated verification key
	"""
	(G, o, g1, g2, e) = params
	# evaluate all lagrange basis polynomial li(0)
	filter = [vk for vk in vks if vk is not None]
	indexes = [i+1 for i, vk in enumerate(vks) if vk is not None]
	l = lagrange_basis(indexes, o) if threshold else [1 for _ in vks]
	# aggregate keys
	aggr_vk = ec_sum([l[i]*filter[i] for i in range(len(filter))])
	return aggr_vk


def sign(params, sk, m):
	"""
	Sign messages.

	Parameters:
		- `params`: public parameters generated by `setup`
		- `sk` (Bn): the secret key of the authority
		- `m` [Bn]: array containing the messages

	Returns:
		- `sigma_tilde` (G1Elem, G1Elem): blinded credential
	"""
	assert len(m) > 0
	(G, o, g1, g2, e) = params
	digest = hash(m)
	h = G.hashG1(digest)
	sigma = sk*h
	return sigma


def aggregate_sigma(params, sigs, threshold=True):
	"""
	Aggregate partial signatures.

	Parameters:
		- `params`: public parameters generated by `setup`
		- `sigs` [G1Elem]: array of partial credentials
		- `threshold` (bool): optional, whether to use threshold cryptography or not

	Returns:
		- `aggr_sigma` (G1Elem): aggregated credential
	"""
	(G, o, g1, g2, e) = params
	# evaluate all lagrange basis polynomial li(0)
	filter = [sig for sig in sigs if sig is not None]
	indexes = [i+1 for i, sig in enumerate(sigs) if sig is not None]
	l = lagrange_basis(indexes, o) if threshold else [1 for _ in sigs]
	# aggregate sigature
	aggr_s = ec_sum([l[i]*filter[i] for i in range(len(filter))])
	return aggr_s


def verify(params, aggr_vk, sigma, m):
	"""
	Verify signature.

	Parameters:
		- `params`: public parameters generated by `setup`
		- `aggr_vk` (G2Elem): aggregated verification key
		- `sigma` (G1Elem): signature
		- `m` [Bn]: array containing the messages

	Returns:
		- `ret` (bool): whether the credential verifies
	"""
	(G, o, g1, g2, e) = params
	digest = hash(m)
	h = G.hashG1(digest)
	return not h.isinf() and e(sigma, g2) == e(h, aggr_vk)
