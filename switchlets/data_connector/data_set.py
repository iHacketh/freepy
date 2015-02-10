# In production, this should ideally be a key value store(read memcache or redis). That's 
# the way it's been designed here

# phone number  -> app name
number_mappings = {
                   '7000' : 'custom_app_1' 
                  }

# app name -> sequence of execution steps in
# a call
app_data = {
            'custom_app_1': [('ivr', 'custom_ivr_1')]
           }

# Another option to store data with such a format
# would be mongodb. 
ivr_info = {
'custom_ivr_1' : [
                    ('short_greeting', ('Say', 'Welcome to company.com please wait \
                    one moment while we transfer you to the main menu.')),

                    ('long_greeting', ('Say',
                      '''Welcome to the main menu.
                      For daily announcement press 1.
                      For company conference room press 2.
                      For departments press 3.'
                      Or to end this call hangup or press pound.''')),

                    ('routes', {
                      '1': ('Play', 'http://some/url/on/the/web'),
                      '2': ('Bridge', { 'endpoint' : 'some conference room'}),
                      '3': ('IVR', [
                                    ('long_greeting', ('Say', 
                                      '''For Sales press 1.
                                      For Billing press 2.
                                      For Human Resources press 3.
                                      For Technical Support press 4.
                                      ''')),

                                    ('routes', {
                                      '1': ('Transfer',{'endpoint' : 'sales'}),
                                      '2': ('Transfer',{'endpoint' : 'billing'}),
                                      '3': ('Transfer',{'endpoint' : 'human resources'}),
                                      '4': ('Transfer',{'endpoint' : 'tech support'})
                                    })
                                  ]
                            ),
                      '#': 'Hangup'}
                    )
                  ]
}