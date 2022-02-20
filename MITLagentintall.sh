export VOLTTRON_HOME=~/.BEMS_3
vctl remove -f  --tag PshaverAgent
vctl remove -f  --tag LPCGMAgent
python scripts/install-agent.py -s PshaverGMagent/ -c PshaverGMagent/config3 -t PshaverAgent
python scripts/install-agent.py -s LPCGMAgent/ -c LPCGMAgent/config3 --t LPCGMAgent
vctl enable  --tag PshaverAgent LPCGMAgent
vctl start  --tag PshaverAgent LPCGMAgent
export VOLTTRON_HOME=~/.BEMS_4
vctl remove -f  --tag PshaverAgent
vctl remove -f  --tag LPCGMAgent

python scripts/install-agent.py -s PshaverGMagent/ -c PshaverGMagent/config4 -t PshaverAgent
python scripts/install-agent.py -s LPCGMAgent/ -c LPCGMAgent/config4 --t LPCGMAgent
vctl enable  --tag PshaverAgent LPCGMAgent
vctl start  --tag PshaverAgent LPCGMAgent

