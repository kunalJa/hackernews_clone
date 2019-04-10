import graphene
from graphene_django import DjangoObjectType
from .models import Link

class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    class Arguments:
        url = graphene.String(required=True)
        description = graphene.String()

    def mutate(self, info, url, description):
        link = Link(url = url, description = description)
        link.save()
        return CreateLink(
            id = link.id,
            url = link.url,
            description = link.description
        )

class RemoveLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        link = Link.objects.get(id=id)
        link.delete()
        return RemoveLink(
            id = id,
            url = link.url,
            description = link.description
        )

class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    remove_link = RemoveLink.Field()
