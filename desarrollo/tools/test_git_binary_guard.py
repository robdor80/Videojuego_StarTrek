"""Integration checks against staged Git blobs, not working-tree sizes."""
import hashlib,json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
GUARD=Path(__file__).with_name('git_binary_guard.py')
POLICY='desarrollo/manifests/git_storage_exceptions.json'
class GuardTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.r=Path(self.tmp.name)
  self.git('init','-q');self.write(POLICY,json.dumps({'exceptions':[]}));self.git('add',POLICY)
 def git(self,*args):return subprocess.check_output(['git',*args],cwd=self.r,stderr=subprocess.STDOUT)
 def write(self,name,data):
  p=self.r/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data.encode() if isinstance(data,str) else data);return p
 def check(self):
  cp=subprocess.run([sys.executable,str(GUARD),'--json'],cwd=self.r,capture_output=True,text=True)
  self.assertIn(cp.returncode,[0,1],cp.stderr);return json.loads(cp.stdout)
 def test_forced_small_uppercase_model_unicode(self):
  self.write('.gitignore','*.GLB\n');self.write('juego/Nave á/Modelo.GLB',b'model');self.git('add','-f','juego')
  self.write('juego/modelos.zip',b'archive');self.git('add','juego/modelos.zip')
  self.assertEqual(len(self.check()['errors']),2)
 def test_size_reads_index_and_exact_boundary(self):
  p=self.write('boundary.dat',b'x'*(25*1024*1024));self.git('add','boundary.dat');p.write_bytes(b'x'*(25*1024*1024+1))
  self.assertFalse(self.check()['errors'])
  self.git('add','boundary.dat');p.write_bytes(b'x');self.assertTrue(self.check()['errors'])
 def test_matching_explicit_exception_only(self):
  data=b'x'*(25*1024*1024+1);self.write('allowed.dat',data);self.git('add','allowed.dat')
  self.write(POLICY,json.dumps({'exceptions':[{'path':'allowed.dat','size':len(data),'sha256':hashlib.sha256(data).hexdigest(),'reason':'test explicit review','approved_by':'test'}]}));self.git('add',POLICY)
  self.assertFalse(self.check()['errors'])
  self.write('allowed.dat',data+b'x');self.git('add','allowed.dat');self.assertTrue(self.check()['errors'])
 def test_metadata_and_unreal_essentials(self):
  for p in ['assets/naves/LICENSE','assets/naves/index.json','assets/naves/.gitkeep','juego/UE5/Test/Content/Blueprint.uasset','juego/UE5/Test/Content/Map.umap','juego/UE5/Test/Config/DefaultEngine.ini']:
   self.write(p,b'fixture');self.git('add',p)
  self.assertFalse(self.check()['errors'])
 def test_labs_and_assets_binary_blocked_under_limit(self):
  self.write('laboratorios/prueba/data.json','{}');self.write('assets/naves/texture.png',b'png');self.git('add','.')
  self.assertEqual(len(self.check()['errors']),2)
 def test_deletion_does_not_scan_working_tree(self):
  self.write('juego/model.fbx',b'model');self.git('add','.');self.git('rm','--cached','juego/model.fbx')
  self.assertFalse(self.check()['errors']);self.assertTrue((self.r/'juego/model.fbx').exists())
if __name__=='__main__':unittest.main()
