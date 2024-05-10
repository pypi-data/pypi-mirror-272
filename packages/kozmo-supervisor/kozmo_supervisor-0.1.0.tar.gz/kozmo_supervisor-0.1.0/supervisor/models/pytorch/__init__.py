from supervisor.utils.missing_optional_dependency import import_optional

ADULTEncoder, ADULTDecoder, MNISTEncoder, MNISTDecoder, MNISTClassifier = import_optional(
    'supervisor.models.pytorch.cfrl_models',
    names=['ADULTEncoder', 'ADULTDecoder', 'MNISTEncoder', 'MNISTDecoder', 'MNISTClassifier'])

HeAE, AE = import_optional('supervisor.models.pytorch.autoencoder', names=['HeAE', 'AE'])
Actor, Critic = import_optional('supervisor.models.pytorch.actor_critic', names=['Actor', 'Critic'])
