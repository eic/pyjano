# janapy

![JANAPY](logo.png) 

*Serve [jana2](https://github.com/JeffersonLab/JANA2) fresh and tasty*


```bash
pip install janapy
```

## jana2 configuration and control in python

```python
import janapy

jana = janapy.create()   # Find jana automatically but it will not work in many cases, so 
                         # create('/path/to/exe') overload should solve this

jana.configure(        
        plugins=[                      # a list of plugins to use:
            'beagle_reader',             # plugin name, no additional parameters
            {'vmeson': {'verbose': 2}}], # add vmeson plugin & set '-Pvmeson:verbose=2' parameter
            
        input="/file/to/process.dat",   # or [list, of, files]
                                                 
        params={                        # for parameters that don't follow <plugin>:<name> naming                        
            'debug_plugin_load': True,   # will work as -Pdebug_plugin_load=1
            'WhateverParam': 42,         # the same here -PWhateverParam        
            'nthreads': 8                # Smart enough to run it like --nthreads=8
        })                               # instead of -P...


# Now we can do many things:
jana.run()           # runs jana with the configuration made above
  
print(jana.config)   # Prints { 'plugins': ['beagle_reader', ...
print(jana.run_args) # Prints -Pplugins=beagle_reader,vmeson ... --nthreads=8
print(jana.result)   # Run stats and success
```

### More on configuration

config.json

```json
{"plugins": ["beagle_reader", "vmeson"], "params": {"debug_plugin_load": true}}                 
```

config.yaml
```yaml
plugins:
    - beagle_reader
    - vmeson:
          verbose: 2   # 0 = silence, 1 = only major, 2 = pretty verbose
    - csv_writer       # This plugin is here to enjoy the comments in yaml
params:                                                
    debug_plugin_load: true   # will work as -Pdebug_plugin_load=1
plugin_dirs:
    /my/plugin/directory      # could it be useful? 
```

Working with configurations:

```python

# Use yaml or JSON
jana.configure(yaml_file='config.yaml')   # BTW, configure method completely overwrites 
jana.configure(json_file='config.json')   # previous configurations. 

jana.append(plugins=['csv_writer'])      # append updates the previous configuration 
jana.run(nthreads=4)                     # might be convenient too
jana.config.update(other_jana.config)    # why not?
 
```

### More on API


```python

# 1. Method chaining
jana = janapy.create().configure(...).log_to('runxxx.log').run()


# 2. Run info and statistics
result = jana.result                  # the result from the last run
print(f"rate: {result.rate}\n" 
      f"events processed: {result.nevents}\n"
      f"input files: {result.input}")


# 3.1 Previous run results might be saved too 
# Why not script things easier?
for n in enumerate(8):
    jana.run(nthreads=n)

xy_data = [(r.nthreads, r.exec_time) for r in jana.results]
plot(xy_data)                                # 


# 4. Async. 
future = jana.run_async()   # Why not result 'future' here  
                            # since 'run' could be pretty long    
```

### Extensions for IPython, GUI, realtime server:

```python
# Extensions for special environemnts
jana.jupyter_control()  # places specialy formatted cell in jupyter notebook

# Starts jana configuration GUI in your browser
jana.web_gui()          # serves configuration GUI in your browser

# Why not pretty print...
jana.result.to_html()   # run report as an HTML
```

### Specially for Thomas

```python
jana.configure(from_mc_wrapper(...))
jana.run(extension=mc_wrapper(...))    # Run this configuration on possible machines
```
