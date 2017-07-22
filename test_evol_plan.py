import unittest
import os
import evol_plan

class EvoTestUtilityFunctions(unittest.TestCase):
	def test_nonetoz_float(self):
		val = evol_plan.nonetoz(.25)
		self.assertEqual(val,.25)
	def test_nonetoz_int(self):
		val = evol_plan.nonetoz(77)
		self.assertEqual(val,77)
	def test_nonetoz_str(self):
		val = evol_plan.nonetoz('.25')
		self.assertEqual(val,.25)
	@unittest.skip('different than none')
	def test_nonetoz_blank(self):
		val = evol_plan.nonetoz()
		self.assertEqual(val,0)
	def test_nonetoz_none(self):
		val = evol_plan.nonetoz(None)
		self.assertEqual(val,0)
	def test_nonetoz_garbage(self):
		val = evol_plan.nonetoz('A')
		self.assertEqual(val,0)

	def test_plan_ref_norm(self):
		pr = evol_plan.plan_ref('D2_1')
		self.assertEqual(pr,'D.D2.D2_1')
	def test_plan_ref_partial(self):
		pr = evol_plan.plan_ref('D2')
		self.assertEqual(pr,'D.D2.D2')
	@unittest.skip('TODO')
	def test_plan_ref_junk(self):
		pr = evol_plan.plan_ref(2)
		self.assertEqual(pr,'D.D2.D2')
	def test_plan_ref_none(self):
		pr = evol_plan.plan_ref(None)
		self.assertEqual(pr,None)

	def test_dash_under_norm(self):
		val = evol_plan.dash_under('D2-1')
		self.assertEqual(val,'D2_1')
	def test_dash_under_none(self):
		val = evol_plan.dash_under(None)
		self.assertEqual(val,None)
	def test_dash_under_none(self):
		val = evol_plan.dash_under(1)
		self.assertEqual(val,'1')

	def test_strip_quotes_double(self):
		val = evol_plan.strip_quotes('ignore the "B" option')
		self.assertEqual(val,'ignore the B option')
	def test_strip_quotes_single(self):
		val = evol_plan.strip_quotes("ignore the 'B' option")
		self.assertEqual(val,'ignore the B option')
	def test_strip_quotes_both(self):
		val = evol_plan.strip_quotes('''ignore the "B's" option''')
		self.assertEqual(val,'ignore the Bs option')
	def test_strip_quotes_single(self):
		val = evol_plan.strip_quotes(None)
		self.assertEqual(val,None)

class EvoTestTeamFunctions(unittest.TestCase):
	def setUp(self):
		evol_plan.teamd = evol_plan.parse_team('Blue:5,Green:3,Red:2')
	def test_parse_team_norm(self):
		val = evol_plan.parse_team('B:2,D:10,E:2,N:5,Z:40')
		self.assertEqual(val,{'B':2, 'D':10, 'E':2, 'N':5, 'Z':40})
	def test_parse_team_spaces(self):
		val = evol_plan.parse_team('  B :2 ,D :10 , E:2,N :  5  ,Z:40  ')
		self.assertEqual(val,{'B':2, 'D':10, 'E':2, 'N':5, 'Z':40})
	def test_parse_team_invalid(self):
		with self.assertRaises(SyntaxError) as raises:
			evol_plan.parse_team('B:2,D:10,E:2,N:5,Z:')
	def test_team_size_norm(self):
		val = evol_plan.team_size('Blue')
		self.assertEqual(val,5)
	def test_team_size_caps(self):
		with self.assertRaises(KeyError) as raises:
			evol_plan.team_size('BLUE')
	def test_define_resources(self):
		of = open('test.tji','w')
		evol_plan.define_resources(of,evol_plan.teamd.keys())
		of.close()
		expected = """resource Blue "Blue" {
  resource Blue1 "Blue1"
  resource Blue2 "Blue2"
  resource Blue3 "Blue3"
  resource Blue4 "Blue4"
  resource Blue5 "Blue5"
}
resource Green "Green" {
  resource Green1 "Green1"
  resource Green2 "Green2"
  resource Green3 "Green3"
}
resource Red "Red" {
  resource Red1 "Red1"
  resource Red2 "Red2"
}
"""
		with open('test.tji','r') as i:
			actual = i.read()
		self.assertEqual(actual,expected)
		os.remove('test.tji')

def rr_helper(value, minct, maxct, maxres):
	v = value.split(',')
	ct = len(v)
	new_minct = min([ct,minct])
	new_maxct = max([ct,maxct])
	numval = [int(n[-1:]) for n in v]
	new_maxres = max([maxres,max(numval)])
	return [new_minct, new_maxct, new_maxres]

#TODO: how to test rand_resource and allocate_resources or perturb_allocations
class EvoTaskRandomTests(unittest.TestCase):
	def setUp(self):
		evol_plan.teamd = evol_plan.parse_team('Blue:5,Green:3,Red:2')
	def test_rand_resource1(self):
		minv1ct = 1
		maxv1ct = 0
		maxv1res = 0
		minv4ct = 1
		maxv4ct = 0
		maxv4res = 0
		minv6ct = 1
		maxv6ct = 0
		maxv6res = 0
		for i in range(0,100):
			v1 = evol_plan.rand_resource('Red',evol_plan.team_size('Red'),1)
			[minv1ct, maxv1ct, maxv1res] = rr_helper(v1, minv1ct, maxv1ct, maxv1res)
			v4 = evol_plan.rand_resource('Green',evol_plan.team_size('Green'),4)
			[minv4ct, maxv4ct, maxv4res] = rr_helper(v4, minv4ct, maxv4ct, maxv4res)
			v6 = evol_plan.rand_resource('Blue',evol_plan.team_size('Blue'),6)
			[minv6ct, maxv6ct, maxv6res] = rr_helper(v6, minv6ct, maxv6ct, maxv6res)
		self.assertTrue(minv1ct==1)
		self.assertTrue(minv4ct==1)
		self.assertTrue(minv6ct==1)
		self.assertTrue(maxv1ct==1)
		self.assertTrue(maxv4ct==2)
		self.assertGreater(maxv6ct,3)
		self.assertLess(maxv6ct,6)
		self.assertTrue(maxv1res==2)
		self.assertTrue(maxv4res==3)
		self.assertEqual(maxv6res,5)

if __name__ == '__main__':
	unittest.main()
