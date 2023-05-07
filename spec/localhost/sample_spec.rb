require 'spec_helper'

describe package('python3.10') do
  it { should be_installed }
end

describe port(8888) do
  it { should be_listening }
end

describe port(27017) do
  it { should be_listening }
end

describe virtualenv(ENV["PWD"] + "/venv") do
  its(:pip_freeze) { should include('cffi' => '1.15.1') }
  its(:pip_freeze) { should include('cryptography' => '40.0.2') }
  its(:pip_freeze) { should include('dnspython' => '2.3.0') }
  its(:pip_freeze) { should include('pyjwt' => '2.6.0') }
  its(:pip_freeze) { should include('pycparser' => '2.21') }
  its(:pip_freeze) { should include('pymongo' => '4.3.3') }
  its(:pip_freeze) { should include('PyYAML' => '6.0') }
  its(:pip_freeze) { should include('tornado' => '6.3') }
end
